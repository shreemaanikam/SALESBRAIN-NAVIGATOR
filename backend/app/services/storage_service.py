import os
import io
import logging
import uuid
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self):
        # We don't initialize clients here to avoid locking in environment state
        # at module import time, but we can cache the s3 client if needed.
        self._s3_client = None

    @property
    def backend(self) -> str:
        is_production = os.getenv("ENVIRONMENT") == "production" or os.getenv("VERCEL_ENV") == "production"
        backend = os.getenv("WORKSPACE_STORAGE_BACKEND", "local").lower()
        if is_production and backend == "local":
            raise RuntimeError("Local storage must NEVER be used as the persistence mechanism in production.")
        return backend

    def _get_s3_client(self):
        # For testing purposes, we can re-evaluate environment variables here
        import boto3
        from botocore.config import Config
        endpoint = os.getenv("OBJECT_STORAGE_ENDPOINT")
        bucket = os.getenv("OBJECT_STORAGE_BUCKET")
        region = os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
        access_key = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
        secret_key = os.getenv("OBJECT_STORAGE_SECRET_KEY")
        
        if not bucket or not access_key or not secret_key:
            raise RuntimeError("S3 storage requested but missing credentials/bucket configuration.")
            
        client = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
            config=Config(signature_version='s3v4')
        )
        return client, bucket

    def _get_local_dir(self):
        local_dir = "/tmp/uploads"
        os.makedirs(local_dir, exist_ok=True)
        return local_dir

    def save_dataframe(self, df: pd.DataFrame, user_id: str, workspace_id: str) -> str:
        """Saves a dataframe to parquet. Returns the storage key."""
        object_key = f"{user_id}/{workspace_id}/dataset.parquet"
        
        # Ensure column names are strings before saving to parquet
        df.columns = df.columns.astype(str)
        
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        if self.backend == "s3":
            client, bucket = self._get_s3_client()
            client.upload_fileobj(buffer, bucket, object_key)
            logger.info(f"Uploaded {object_key} to S3 bucket {bucket}")
        else:
            local_dir = self._get_local_dir()
            local_path = os.path.join(local_dir, object_key.replace("/", "_"))
            with open(local_path, "wb") as f:
                f.write(buffer.read())
            logger.info(f"Saved {object_key} to local path {local_path}")
            object_key = local_path # For local we just return the path directly for easier loading
            
        return object_key

    def load_dataframe(self, object_key: str) -> pd.DataFrame:
        """Loads a dataframe from the given object key."""
        if self.backend == "s3":
            client, bucket = self._get_s3_client()
            buffer = io.BytesIO()
            client.download_fileobj(bucket, object_key, buffer)
            buffer.seek(0)
            return pd.read_parquet(buffer)
        else:
            if not os.path.exists(object_key):
                raise FileNotFoundError(f"Local file missing: {object_key}")
            return pd.read_parquet(object_key)

    def delete_object(self, object_key: str) -> None:
        """Deletes the object key from storage."""
        if not object_key:
            return
            
        if self.backend == "s3":
            client, bucket = self._get_s3_client()
            try:
                client.delete_object(Bucket=bucket, Key=object_key)
                logger.info(f"Deleted {object_key} from S3")
            except Exception as e:
                logger.error(f"Failed to delete {object_key} from S3: {e}")
        else:
            if os.path.exists(object_key):
                os.remove(object_key)
                logger.info(f"Deleted {object_key} from local storage")

storage_service = StorageService()
