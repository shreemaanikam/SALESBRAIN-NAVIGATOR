"""
Tests for My Data Workspace endpoints.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.app.main import app
from backend.app.services.workspace_service import workspace_registry

client = TestClient(app)

def test_dataset_upload_and_lifecycle():
    # 1. Upload a valid CSV
    csv_content = b"order_id,sales,profit,category,order_date\n1,100,20,A,2023-01-01\n2,200,-10,B,2023-01-02\n3,150,5,A,2023-01-03"
    response = client.post(
        "/api/v1/datasets/upload",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "dataset_id" in data
    dataset_id = data["dataset_id"]
    assert data["row_count"] == 3
    assert data["column_count"] == 5
    
    # 2. List datasets
    res_list = client.get("/api/v1/datasets")
    assert res_list.status_code == 200
    assert any(d["dataset_id"] == dataset_id for d in res_list.json()["datasets"])
    
    # 3. Get Preview
    res_prev = client.get(f"/api/v1/datasets/{dataset_id}/preview")
    assert res_prev.status_code == 200
    assert len(res_prev.json()["records"]) == 3
    
    # 4. Map Columns
    mapping = {
        "order_id": "order_id",
        "sales": "sales",
        "profit": "profit",
        "category": "category",
        "order_date": "order_date"
    }
    res_map = client.post(
        f"/api/v1/datasets/{dataset_id}/map-columns",
        json={"mapping": mapping}
    )
    assert res_map.status_code == 200
    assert res_map.json()["validation"]["valid"] is True
    
    # 5. Create Dashboard
    res_dash = client.post(f"/api/v1/datasets/{dataset_id}/create-dashboard")
    assert res_dash.status_code == 200
    dash_data = res_dash.json()["dashboard"]
    assert "kpis" in dash_data
    assert "category_breakdown" in dash_data
    
    # 6. Generate Insights
    res_ins = client.post(f"/api/v1/datasets/{dataset_id}/generate-insights")
    assert res_ins.status_code == 200
    assert "count" in res_ins.json()
    
    # 7. Generate Recommendations
    res_rec = client.post(f"/api/v1/datasets/{dataset_id}/generate-recommendations")
    assert res_rec.status_code == 200
    assert "count" in res_rec.json()
    
    # 8. Export CSV
    res_export = client.get(f"/api/v1/datasets/{dataset_id}/export?report_type=kpis")
    assert res_export.status_code == 200
    assert res_export.headers["content-type"] == "text/csv; charset=utf-8"
    
    # 9. Delete Workspace
    res_del = client.delete(f"/api/v1/datasets/{dataset_id}")
    assert res_del.status_code == 200
    assert workspace_registry.get(dataset_id) is None
