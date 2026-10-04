import pytest
import pandas as pd
import os
import io
from unittest.mock import patch, MagicMock
from backend.app.services.storage_service import StorageService

@pytest.fixture
def sample_df():
    return pd.DataFrame({"col1": [1, 2], "col2": ["A", "B"]})

def test_local_storage(sample_df, tmp_path):
    with patch.dict("os.environ", {"WORKSPACE_STORAGE_BACKEND": "local", "ENVIRONMENT": "development"}):
        storage = StorageService()
        with patch.object(storage, '_get_local_dir', return_value=str(tmp_path)):
            # Save
            key = storage.save_dataframe(sample_df, "user1", "ws1")
            assert key == os.path.join(str(tmp_path), "user1_ws1_dataset.parquet")
            
            # Load
            loaded_df = storage.load_dataframe(key)
            assert len(loaded_df) == 2
            assert list(loaded_df.columns) == ["col1", "col2"]
            assert list(loaded_df["col1"].values) == [1, 2]
            
            # Delete
            storage.delete_object(key)
            assert not os.path.exists(key)

@patch("boto3.client")
def test_s3_storage(mock_boto_client, sample_df):
    mock_s3 = MagicMock()
    mock_boto_client.return_value = mock_s3
    
    with patch.dict("os.environ", {
        "WORKSPACE_STORAGE_BACKEND": "s3",
        "OBJECT_STORAGE_ENDPOINT": "https://mock-s3",
        "OBJECT_STORAGE_BUCKET": "mock-bucket",
        "OBJECT_STORAGE_ACCESS_KEY": "acc",
        "OBJECT_STORAGE_SECRET_KEY": "sec",
        "ENVIRONMENT": "development"
    }):
        storage = StorageService()
        
        # Save
        key = storage.save_dataframe(sample_df, "user2", "ws2")
        assert key == "user2/ws2/dataset.parquet"
        mock_s3.upload_fileobj.assert_called_once()
        
        # Load
        def mock_download_fileobj(bucket, key, buffer):
            sample_df.to_parquet(buffer, index=False)
            
        mock_s3.download_fileobj = mock_download_fileobj
        loaded_df = storage.load_dataframe(key)
        assert len(loaded_df) == 2
        
        # Delete
        storage.delete_object(key)
        mock_s3.delete_object.assert_called_once_with(Bucket="mock-bucket", Key=key)

def test_s3_missing_credentials():
    with patch.dict("os.environ", {
        "WORKSPACE_STORAGE_BACKEND": "s3",
        "OBJECT_STORAGE_BUCKET": "",
        "OBJECT_STORAGE_ACCESS_KEY": "",
        "OBJECT_STORAGE_SECRET_KEY": "",
    }, clear=True):
        storage = StorageService()
        with pytest.raises(RuntimeError, match="missing credentials/bucket configuration"):
            storage.save_dataframe(pd.DataFrame(), "u", "w")

def test_production_refuses_local():
    with patch.dict("os.environ", {
        "ENVIRONMENT": "production",
        "WORKSPACE_STORAGE_BACKEND": "local"
    }):
        storage = StorageService()
        with pytest.raises(RuntimeError, match="Local storage must NEVER be used as the persistence mechanism in production."):
            _ = storage.backend
