import os
import io
import logging
import uuid
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)

# Determine if we should use S3 or Local storage
STORAGE_BACKEND = os.getenv("WORKSPACE_STORAGE_BACKEND", "local").lower()

class StorageService:
    def __init__(self):
        self.backend = STORAGE_BACKEND
        if self.backend == "s3":
            import boto3
            from botocore.config import Config
            self.endpoint = os.getenv("OBJECT_STORAGE_ENDPOINT")
            self.bucket = os.getenv("OBJECT_STORAGE_BUCKET")
            self.region = os.getenv("OBJECT_STORAGE_REGION", "us-east-1")
            self.access_key = os.getenv("OBJECT_STORAGE_ACCESS_KEY")
            self.secret_key = os.getenv("OBJECT_STORAGE_SECRET_KEY")
            
            if not self.bucket or not self.access_key or not self.secret_key:
                raise RuntimeError("S3 storage requested but missing credentials/bucket configuration.")
                
            self.s3 = boto3.client(
                's3',
                endpoint_url=self.endpoint,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region,
                config=Config(signature_version='s3v4')
            )
            logger.info(f"Initialized S3 storage using bucket: {self.bucket}")
        else:
            self.local_dir = "backend/app/data/uploads"
            os.makedirs(self.local_dir, exist_ok=True)
            logger.info(f"Initialized Local storage at {self.local_dir}")

    def save_dataframe(self, df: pd.DataFrame, user_id: str, workspace_id: str) -> str:
        """Saves a dataframe to parquet. Returns the storage key."""
        object_key = f"{user_id}/{workspace_id}/dataset.parquet"
        
        # Ensure column names are strings before saving to parquet
        df.columns = df.columns.astype(str)
        
        buffer = io.BytesIO()
        df.to_parquet(buffer, index=False)
        buffer.seek(0)
        
        if self.backend == "s3":
            self.s3.upload_fileobj(buffer, self.bucket, object_key)
            logger.info(f"Uploaded {object_key} to S3 bucket {self.bucket}")
        else:
            # We replace slashes with underscores for local storage to keep it flat or recreate dirs
            local_path = os.path.join(self.local_dir, object_key.replace("/", "_"))
            with open(local_path, "wb") as f:
                f.write(buffer.read())
            logger.info(f"Saved {object_key} to local path {local_path}")
            object_key = local_path # For local we just return the path directly for easier loading
            
        return object_key

    def load_dataframe(self, object_key: str) -> pd.DataFrame:
        """Loads a dataframe from the given object key."""
        if self.backend == "s3":
            buffer = io.BytesIO()
            self.s3.download_fileobj(self.bucket, object_key, buffer)
            buffer.seek(0)
            return pd.read_parquet(buffer)
        else:
            # Local fallback uses the path directly
            if not os.path.exists(object_key):
                raise FileNotFoundError(f"Local file missing: {object_key}")
            return pd.read_parquet(object_key)

    def delete_object(self, object_key: str) -> None:
        """Deletes the object key from storage."""
        if not object_key:
            return
            
        if self.backend == "s3":
            try:
                self.s3.delete_object(Bucket=self.bucket, Key=object_key)
                logger.info(f"Deleted {object_key} from S3")
            except Exception as e:
                logger.error(f"Failed to delete {object_key} from S3: {e}")
        else:
            if os.path.exists(object_key):
                os.remove(object_key)
                logger.info(f"Deleted {object_key} from local storage")

storage_service = StorageService()
