import pytest
import pandas as pd
from backend.app.services.workspace_service import profile_columns, validate_mapping, compute_dashboard

def test_financial_headers_do_not_overmap():
    # Test OHLC dataset
    df = pd.DataFrame({
        "date": ["2023-01-01"],
        "open": [10.0],
        "high": [11.0],
        "low": [9.0],
        "close": [10.5],
        "volume": [100]
    })
    res = profile_columns(df)
    suggested = res["suggested_mapping"]
    
    # ensure "open" is not mapped to sales
    assert suggested.get("sales") != "open"
    # ensure "high" is not mapped to product_id
    assert suggested.get("product_id") != "high"
    # ensure "close" is not mapped to order_priority
    assert suggested.get("order_priority") != "close"
    
    # date can map to order_date
    assert suggested.get("order_date") == "date"
    # but since it's mapped, ship_date shouldn't map to date
    assert suggested.get("ship_date") != "date"


def test_duplicate_mapping_validation_fails():
    df = pd.DataFrame({"open": [10.0], "volume": [100]})
    # duplicate mapping
    mapping = {
        "sales": "open",
        "product_id": "open"
    }
    val = validate_mapping(df, mapping)
    assert val["valid"] is False
    assert any("mapped multiple times" in err for err in val["errors"])


def test_dashboard_computation_safe_groupby():
    # Even if they bypass validation and force a duplicate mapping, dashboard should not crash
    df = pd.DataFrame({"open": [10.0, 20.0]})
    mapping = {
        "sales": "open",
        "category": "open", # Both mapped to open
        "product_id": "open",
        "region": "open",
        "segment": "open"
    }
    # this used to crash with "cannot insert open, already exists"
    dash = compute_dashboard(df, mapping)
    
    # It should not crash.
    assert dash is not None

def test_missing_sales_warning():
    df = pd.DataFrame({"open": [10.0], "volume": [100]})
    mapping = {"category": "volume"}
    val = validate_mapping(df, mapping)
    assert any("No 'sales' column mapped" in w for w in val["warnings"])

def test_dashboard_sales_trend_no_crash_on_str():
    df = pd.DataFrame({
        "order_date": ["2023-01-01", "2023-02-01"],
        "sales": [100.0, 200.0],
        "profit": [10.0, 20.0]
    })
    mapping = {
        "order_date": "order_date",
        "sales": "sales",
        "profit": "profit"
    }
    dash = compute_dashboard(df, mapping)
    assert dash["sales_trend"] is not None
    assert len(dash["sales_trend"]) == 2

