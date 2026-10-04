import json
import pytest
from pathlib import Path

def test_ml_metadata_test_size():
    metadata_path = Path("backend/app/ml/artifacts/model_metadata.json")
    assert metadata_path.exists(), "Model metadata must exist"
    
    with open(metadata_path, "r") as f:
        meta = json.load(f)
        
    assert meta["split_info"]["test_size"] > 0, "ML test size must be > 0 to compute valid metrics"
    assert meta["metrics"]["r2"] is not None
    assert meta["metrics"]["mae"] is not None

def test_ml_missing_feature_prevention():
    from backend.app.services.prediction_service import prediction_service
    import pandas as pd
    
    df = pd.DataFrame({
        "category": ["A"], "sub_category": ["A1"], "segment": ["B"],
        "region": ["C"], "market": ["D"], "ship_mode": ["E"],
        "sales": [100.0], "quantity": [2], "discount": [0.1]
    })
    mapping = {c: c for c in df.columns}
    
    with pytest.raises(ValueError, match="Dataset incompatible"):
        prediction_service.predict_batch(df, mapping)

def test_dashboard_works_without_ml():
    from backend.app.services.workspace_service import compute_dashboard
    import pandas as pd
    
    df = pd.DataFrame({
        "sales": [100.0, 200.0],
        "profit": [10.0, 20.0]
    })
    mapping = {"sales": "sales", "profit": "profit"}
    
    dashboard = compute_dashboard(df, mapping)
    assert dashboard is not None
    assert "kpis" in dashboard

def test_actual_vs_predicted_separation():
    from backend.app.services.prediction_service import prediction_service
    import pandas as pd
    
    df = pd.DataFrame({
        "category": ["A"], "sub_category": ["A1"], "segment": ["B"],
        "region": ["C"], "market": ["D"], "ship_mode": ["E"],
        "sales": [100.0], "quantity": [2], "discount": [0.1], "shipping_cost": [5.0]
    })
    mapping = {c: c for c in df.columns}
    
    res = prediction_service.predict_batch(df, mapping)
    assert res is not None
    assert isinstance(res, pd.Series)
