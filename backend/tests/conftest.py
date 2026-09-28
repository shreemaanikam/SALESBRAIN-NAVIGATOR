import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.database import Base, engine, get_db
from backend.app.api.deps import get_current_user

# Setup testing DB
Base.metadata.create_all(bind=engine)

def override_get_current_user():
    return "test_user_id"

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
