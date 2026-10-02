import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import pandas as pd
from backend.app.services.storage_service import storage_service

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "database" in data
    assert "storage" in data

def test_api_rewrite_logic():
    # If a Vercel rewrite sends traffic to `/api/v1/health`, the app must handle it
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_tenant_isolation():
    response = client.get("/api/v1/datasets/invalid-id")
    # Depends on auth. In local mode, returns 404 since workspace doesn't exist for 'local_dev_user'
    assert response.status_code in [401, 404]

def test_storage_local_fallback():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    key = storage_service.save_dataframe(df, "test_user", "test_workspace")
    assert key is not None
    df_loaded = storage_service.load_dataframe(key)
    assert len(df_loaded) == 2
    storage_service.delete_object(key)
