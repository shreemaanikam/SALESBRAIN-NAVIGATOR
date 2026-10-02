import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from backend.app.services.storage_service import StorageService

@pytest.fixture
def sample_df():
    return pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})

def test_local_storage(sample_df, tmp_path):
    with patch("backend.app.services.storage_service.STORAGE_BACKEND", "local"):
        storage = StorageService()
        storage.local_dir = str(tmp_path)
        
        # Save
        key = storage.save_dataframe(sample_df, "user1", "ws1")
        assert key.endswith("user1_ws1_dataset.parquet")
        
        # Load
        loaded_df = storage.load_dataframe(key)
        assert len(loaded_df) == 2
        assert list(loaded_df.columns) == ["col1", "col2"]
        
        # Delete
        storage.delete_object(key)
        assert not os.path.exists(key)

@patch("boto3.client")
def test_s3_storage(mock_boto3, sample_df):
    with patch.dict("os.environ", {
        "WORKSPACE_STORAGE_BACKEND": "s3",
        "OBJECT_STORAGE_ENDPOINT": "https://mock-s3",
        "OBJECT_STORAGE_BUCKET": "mock-bucket",
        "OBJECT_STORAGE_ACCESS_KEY": "acc",
        "OBJECT_STORAGE_SECRET_KEY": "sec"
    }):
        storage = StorageService()
        
        # Save
        key = storage.save_dataframe(sample_df, "user2", "ws2")
        assert key == "user2/ws2/dataset.parquet"
        storage.s3.upload_fileobj.assert_called_once()
        
        # Load
        # we need to mock download_fileobj to actually write parquet to the buffer
        def mock_download_fileobj(bucket, key, buffer):
            sample_df.to_parquet(buffer, index=False)
            
        storage.s3.download_fileobj = mock_download_fileobj
        loaded_df = storage.load_dataframe(key)
        assert len(loaded_df) == 2
        
        # Delete
        storage.delete_object(key)
        storage.s3.delete_object.assert_called_once_with(Bucket="mock-bucket", Key=key)
