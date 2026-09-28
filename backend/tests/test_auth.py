import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.api.deps import get_current_user
import os

def test_missing_token_production():
    # Remove override
    app.dependency_overrides.clear()
    
    # Mock production environment
    os.environ["RENDER"] = "true"
    
    with TestClient(app) as client:
        response = client.get("/api/v1/datasets")
        assert response.status_code == 500 # local mode in production fails closed
        
    os.environ["RENDER"] = "false"
    os.environ["AUTH_MODE"] = "firebase"
    
    with TestClient(app) as client:
        response = client.get("/api/v1/datasets")
        assert response.status_code == 401 # firebase mode fails without token

def test_tenant_isolation():
    app.dependency_overrides.clear()
    
    # Create user A workspace
    def override_user_a(): return "user_a"
    app.dependency_overrides[get_current_user] = override_user_a
    with TestClient(app) as client:
        csv_data = "Date,Sales\n2023-01-01,100"
        res = client.post("/api/v1/datasets/upload", files={"file": ("test.csv", csv_data, "text/csv")})
        assert res.status_code == 200
        dataset_a = res.json()["dataset_id"]
        
        # Verify user A sees it
        res_list = client.get("/api/v1/datasets")
        assert any(d["dataset_id"] == dataset_a for d in res_list.json()["datasets"])
        
    # Create user B workspace
    def override_user_b(): return "user_b"
    app.dependency_overrides[get_current_user] = override_user_b
    with TestClient(app) as client:
        # Verify user B does NOT see it
        res_list = client.get("/api/v1/datasets")
        assert not any(d["dataset_id"] == dataset_a for d in res_list.json()["datasets"])
        
        # Verify user B cannot access user A dataset directly
        res_get = client.get(f"/api/v1/datasets/{dataset_a}/insights")
        assert res_get.status_code == 404

def test_legacy_workspace_isolation():
    app.dependency_overrides.clear()
    
    # Create a legacy workspace directly in DB
    from backend.app.db.database import SessionLocal
    from backend.app.db.models import Workspace
    import uuid
    
    db = SessionLocal()
    legacy_id = str(uuid.uuid4())
    ws = Workspace(id=legacy_id, filename="legacy.csv", filepath="dummy", user_id="legacy_user")
    db.add(ws)
    db.commit()
    db.close()
    
    # Authenticate as a new firebase user
    def override_new_user(): return "new_firebase_uid"
    app.dependency_overrides[get_current_user] = override_new_user
    
    with TestClient(app) as client:
        # Verify the new user cannot see legacy workspace
        res_list = client.get("/api/v1/datasets")
        assert not any(d["dataset_id"] == legacy_id for d in res_list.json()["datasets"])
        
        # Verify direct access fails
        res_get = client.get(f"/api/v1/datasets/{legacy_id}/insights")
        assert res_get.status_code == 404
