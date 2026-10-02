import pytest
from fastapi.testclient import TestClient

def test_vercel_entrypoint_import():
    try:
        from backend.api.index import app
        assert app is not None
        assert app.title == "SalesBrain Navigator"
    except ImportError as e:
        pytest.fail(f"Failed to import Vercel entrypoint: {e}")

def test_upload_limit_enforced():
    # Verify the code has the 4.5MB limit
    from backend.app.api.v1.routes.datasets import MAX_FILE_SIZE_BYTES
    assert MAX_FILE_SIZE_BYTES == 4.5 * 1024 * 1024
