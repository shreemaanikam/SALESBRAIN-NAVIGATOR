import pytest
import pandas as pd
from backend.app.services.workspace_service import validate_mapping, compute_dashboard

def test_invalid_numeric_values():
    df = pd.DataFrame({"sales": ["apple", "banana", "cherry"]})
    mapping = {"sales": "sales"}
    val = validate_mapping(df, mapping)
    assert not val["valid"]
    assert any("non-numeric" in err for err in val["errors"])

def test_missing_optional_fields():
    df = pd.DataFrame({"sales": [10.0, 20.0]})
    mapping = {"sales": "sales"}
    val = validate_mapping(df, mapping)
    assert val["valid"]
    dash = compute_dashboard(df, mapping)
    assert dash["kpis"][0]["label"] == "Total Sales"
    assert dash["profitability_quadrant"] is None

def test_missing_required_fields():
    df = pd.DataFrame({"category": ["A", "B"]})
    mapping = {"category": "category"}
    val = validate_mapping(df, mapping)
    # validate_mapping itself doesn't enforce "sales", it just warns.
    assert any("No 'sales' column mapped" in w for w in val["warnings"])

def test_empty_dataset_handling():
    df = pd.DataFrame(columns=["sales", "category"])
    mapping = {"sales": "sales", "category": "category"}
    # Dashboard should just compute zeros/empty
    dash = compute_dashboard(df, mapping)
    assert dash["kpis"][0]["raw"] == 0.0

def test_correct_dashboard_totals():
    df = pd.DataFrame({
        "sales": [100.0, 200.0, 300.0],
        "profit": [10.0, -20.0, 30.0],
        "category": ["A", "B", "A"]
    })
    mapping = {"sales": "sales", "profit": "profit", "category": "category"}
    dash = compute_dashboard(df, mapping)
    
    kpi_dict = {k["label"]: k["raw"] for k in dash["kpis"]}
    assert kpi_dict["Total Sales"] == 600.0
    assert kpi_dict["Total Profit"] == 20.0
    
    cat = dash["category_breakdown"]
    assert len(cat) == 2
    # category A should have 400 sales, 40 profit
    cat_a = next(c for c in cat if c["name"] == "A")
    assert cat_a["value"] == 400.0
    assert cat_a["profit"] == 40.0
