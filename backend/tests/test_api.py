"""
SalesBrain Navigator — Backend Test Suite

Tests for data validation, API endpoints, prediction, and analytics.
"""

import os
import sys
import json
import pytest
import pandas as pd
import numpy as np

# Ensure the project root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


# ============================================================
# Health & Metadata
# ============================================================

class TestHealth:
    def test_health_returns_ok(self):
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "version" in data
        assert "timestamp" in data
        assert "dataset_ready" in data
        assert "model_ready" in data

    def test_metadata_returns_dataset_info(self):
        r = client.get("/api/v1/metadata")
        assert r.status_code == 200
        data = r.json()
        assert "dataset" in data
        assert "model" in data


# ============================================================
# Dashboard KPIs
# ============================================================

class TestDashboard:
    def test_kpis_returns_metrics(self):
        r = client.get("/api/v1/dashboard/kpis")
        assert r.status_code == 200
        data = r.json()
        assert "metrics" in data
        metrics = data["metrics"]
        assert len(metrics) >= 4
        labels = [m["label"] for m in metrics]
        assert "Total Sales" in labels
        assert "Total Profit" in labels

    def test_kpis_total_sales_correct(self):
        r = client.get("/api/v1/dashboard/kpis")
        metrics = {m["label"]: m["value"] for m in r.json()["metrics"]}
        # Total sales should be approximately 12.64M
        sales_str = metrics["Total Sales"]
        assert "12,642,905" in sales_str or "12642905" in sales_str

    def test_trends_returns_data(self):
        r = client.get("/api/v1/dashboard/trends")
        assert r.status_code == 200
        data = r.json()
        assert "data" in data
        assert len(data["data"]) > 0


# ============================================================
# Sales Analytics
# ============================================================

class TestSales:
    def test_sales_by_category(self):
        r = client.get("/api/v1/sales/by-category")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        categories = [d["category"] for d in data]
        assert "Technology" in categories
        assert "Furniture" in categories
        assert "Office Supplies" in categories

    def test_sales_by_region(self):
        r = client.get("/api/v1/sales/by-region")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0

    def test_sales_by_market(self):
        r = client.get("/api/v1/sales/by-market")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0

    def test_monthly_sales(self):
        r = client.get("/api/v1/sales/monthly")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0


# ============================================================
# Products
# ============================================================

class TestProducts:
    def test_product_list(self):
        r = client.get("/api/v1/products?page=1&page_size=5")
        assert r.status_code == 200
        data = r.json()
        assert "products" in data
        assert "total" in data
        assert len(data["products"]) <= 5

    def test_product_search(self):
        r = client.get("/api/v1/products?q=Canon")
        assert r.status_code == 200
        data = r.json()
        # Canon products should appear
        assert data["total"] > 0

    def test_product_filter_by_category(self):
        r = client.get("/api/v1/products?category=Technology&page_size=5")
        assert r.status_code == 200
        data = r.json()
        for p in data["products"]:
            assert p["category"] == "Technology"

    def test_product_detail_valid(self):
        # First get a real product_id
        r = client.get("/api/v1/products?page_size=1")
        product_id = r.json()["products"][0]["product_id"]
        r2 = client.get(f"/api/v1/products/{product_id}")
        assert r2.status_code == 200

    def test_product_detail_404(self):
        r = client.get("/api/v1/products/INVALID-PRODUCT-99999")
        assert r.status_code == 404


# ============================================================
# Customers
# ============================================================

class TestCustomers:
    def test_customer_segments(self):
        r = client.get("/api/v1/customers/segments")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        segments = [d["segment"] for d in data]
        assert "Consumer" in segments


# ============================================================
# Geography
# ============================================================

class TestGeography:
    def test_geography_summary(self):
        r = client.get("/api/v1/geography/summary")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0

    def test_geography_countries(self):
        r = client.get("/api/v1/geography/countries")
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0


# ============================================================
# Profitability
# ============================================================

class TestProfitability:
    def test_profitability_summary(self):
        r = client.get("/api/v1/profitability/summary")
        assert r.status_code == 200


# ============================================================
# Outliers
# ============================================================

class TestOutliers:
    def test_outlier_detection(self):
        r = client.get("/api/v1/outliers")
        assert r.status_code == 200
        data = r.json()
        assert "lower_fence" in data
        assert "upper_fence" in data
        assert "total_outliers" in data
        assert "outlier_pct" in data
        # Validate against reference values
        assert data["lower_fence"] == -299.0
        assert data["upper_fence"] == 581.0
        assert data["total_outliers"] == 5655
        assert abs(data["outlier_pct"] - 11.03) < 0.1


# ============================================================
# Data Explorer
# ============================================================

class TestDataExplorer:
    def test_data_schema(self):
        r = client.get("/api/v1/data/schema")
        assert r.status_code == 200

    def test_data_quality(self):
        r = client.get("/api/v1/data/quality")
        assert r.status_code == 200


# ============================================================
# Predictions
# ============================================================

class TestPredictions:
    def test_model_status(self):
        r = client.get("/api/v1/models/status")
        assert r.status_code == 200
        data = r.json()
        assert "available" in data

    def test_predict_profit(self):
        r = client.post("/api/v1/predictions/profit", json={
            "category": "Technology",
            "sub_category": "Phones",
            "segment": "Consumer",
            "region": "West",
            "market": "US",
            "ship_mode": "Standard Class",
            "sales": 500.0,
            "quantity": 3,
            "discount": 0.1,
            "shipping_cost": 15.0
        })
        assert r.status_code == 200
        data = r.json()
        assert "predicted_profit" in data
        assert "model_name" in data
        assert "caveat" in data

    def test_predict_invalid_input(self):
        r = client.post("/api/v1/predictions/profit", json={
            "category": "Technology"
            # Missing required fields
        })
        assert r.status_code == 422


# ============================================================
# Insights & Recommendations
# ============================================================

class TestInsights:
    def test_insights(self):
        r = client.get("/api/v1/insights")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_recommendations(self):
        r = client.get("/api/v1/recommendations")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if len(data) > 0:
            rec = data[0]
            assert "id" in rec
            assert "title" in rec
            assert "source" in rec


# ============================================================
# Scenarios
# ============================================================

class TestScenarios:
    def test_simulate(self):
        r = client.post("/api/v1/simulate", json={
            "baseline": {
                "category": "Technology",
                "sub_category": "Phones",
                "segment": "Consumer",
                "region": "West",
                "market": "US",
                "ship_mode": "Standard Class",
                "sales": 500.0,
                "quantity": 3,
                "discount": 0.1,
                "shipping_cost": 15.0
            },
            "scenario": {
                "discount_delta": -0.05,
                "quantity_change_pct": 10.0,
                "shipping_cost_change_pct": 5.0
            }
        })
        assert r.status_code == 200
        data = r.json()
        assert "baseline_profit" in data
        assert "scenario_profit" in data
        assert "absolute_delta" in data


# ============================================================
# Reports
# ============================================================

class TestReports:
    def test_report_types(self):
        r = client.get("/api/v1/reports/types")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_export_csv(self):
        r = client.post("/api/v1/reports/export", json={
            "report_type": "sales",
            "format": "csv"
        })
        assert r.status_code == 200
        assert "text/csv" in r.headers.get("content-type", "") or len(r.content) > 0


# ============================================================
# Data Reconciliation
# ============================================================

class TestReconciliation:
    """Verify API aggregates match direct computation from CSV."""

    @pytest.fixture(autouse=True)
    def load_reference(self):
        df = pd.read_csv("dataset/Cleaned_SuperStore.csv")
        self.total_sales = float(df["sales"].sum())
        self.total_profit = float(df["profit"].sum())
        self.unique_orders = int(df["order_id"].nunique())
        self.row_count = len(df)

    def test_total_sales_reconciliation(self):
        r = client.get("/api/v1/dashboard/kpis")
        metrics = {m["label"]: m["value"] for m in r.json()["metrics"]}
        api_sales = float(metrics["Total Sales"].replace("$", "").replace(",", ""))
        assert abs(api_sales - self.total_sales) < 1.0, (
            f"API={api_sales}, CSV={self.total_sales}"
        )

    def test_total_profit_reconciliation(self):
        r = client.get("/api/v1/dashboard/kpis")
        metrics = {m["label"]: m["value"] for m in r.json()["metrics"]}
        api_profit = float(metrics["Total Profit"].replace("$", "").replace(",", ""))
        assert abs(api_profit - self.total_profit) < 1.0, (
            f"API={api_profit}, CSV={self.total_profit}"
        )

    def test_unique_orders_reconciliation(self):
        r = client.get("/api/v1/dashboard/kpis")
        metrics = {m["label"]: m["value"] for m in r.json()["metrics"]}
        api_orders = int(metrics["Unique Orders"].replace(",", ""))
        assert api_orders == self.unique_orders

    def test_category_sales_reconciliation(self):
        r = client.get("/api/v1/sales/by-category")
        api_data = {d["category"]: d["sales"] for d in r.json()}
        df = pd.read_csv("dataset/Cleaned_SuperStore.csv")
        csv_data = df.groupby("category")["sales"].sum()
        for cat in ["Technology", "Furniture", "Office Supplies"]:
            assert abs(api_data[cat] - float(csv_data[cat])) < 1.0, (
                f"{cat}: API={api_data[cat]}, CSV={float(csv_data[cat])}"
            )

    def test_outlier_stats_reconciliation(self):
        r = client.get("/api/v1/outliers")
        data = r.json()
        df = pd.read_csv("dataset/Cleaned_SuperStore.csv")
        q1 = df["sales"].quantile(0.25)
        q3 = df["sales"].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((df["sales"] < lower) | (df["sales"] > upper)).sum())
        assert data["lower_fence"] == lower
        assert data["upper_fence"] == upper
        assert data["total_outliers"] == outlier_count

def test_inf_handling():
    from backend.app.data.validation import clean_for_json
    import numpy as np
    import pandas as pd
    
    # Test clean_for_json handles infinity and NaN safely
    assert clean_for_json(np.nan) is None
    assert clean_for_json(pd.NA) is None
    assert clean_for_json(float('inf')) is None
    assert clean_for_json(float('-inf')) is None
    assert clean_for_json(np.inf) is None
    assert clean_for_json(-np.inf) is None
    assert clean_for_json(10.5) == 10.5
    assert clean_for_json(10) == 10
