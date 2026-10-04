from backend.app.services.storage_service import storage_service
"""
SalesBrain Navigator — Workspace Service
Handles user-uploaded dataset lifecycle: storage, profiling, analytics, insights, recommendations.
All workspaces are in-memory (demo mode). Cleared on server restart.
"""

import io
import uuid
import logging
import pandas as pd
from backend.app.services.storage_service import storage_service
import numpy as np
from typing import Dict, Any, List, Optional
from backend.app.services.prediction_service import prediction_service
from datetime import datetime

logger = logging.getLogger("SalesBrain")

# ──────────────────────────────────────────────────────────────────────────────
# Column mapping hints: business concept → list of likely source column names
# ──────────────────────────────────────────────────────────────────────────────
CONCEPT_HINTS: Dict[str, List[str]] = {
    "order_id":       ["order_id", "order_number", "transaction_id", "id", "order"],
    "order_date":     ["order_date", "purchase_date", "date", "order_dt", "sale_date", "transaction_date"],
    "ship_date":      ["ship_date", "delivery_date", "shipped_date", "delivered_date"],
    "product_name":   ["product_name", "product", "item", "item_name", "name", "description"],
    "product_id":     ["product_id", "sku", "item_id", "product_code"],
    "category":       ["category", "product_category", "cat", "dept", "department"],
    "sub_category":   ["sub_category", "subcategory", "sub_cat", "product_type", "type"],
    "sales":          ["sales", "revenue", "amount", "total", "sale_amount", "gross_sales"],
    "profit":         ["profit", "net_profit", "net", "margin_amount", "gross_profit"],
    "quantity":       ["quantity", "units", "qty", "count", "sold"],
    "discount":       ["discount", "discount_rate", "disc", "promo"],
    "shipping_cost":  ["shipping_cost", "delivery_cost", "freight", "shipping"],
    "region":         ["region", "territory", "zone", "area"],
    "country":        ["country", "nation", "country_name"],
    "market":         ["market", "geo_market"],
    "segment":        ["segment", "customer_segment", "customer_type", "cust_segment"],
    "ship_mode":      ["ship_mode", "shipping_method", "delivery_method", "ship_type"],
    "order_priority": ["order_priority", "priority", "urgency"],
    "state":          ["state", "province", "state_name"],
    "customer_name":  ["customer_name", "customer", "client", "client_name"],
}

REQUIRED_CONCEPTS = []  # No hard requirements — analytics adapt to what's available
SALES_CONCEPTS = ["sales"]
PROFIT_CONCEPTS = ["profit"]
DATE_CONCEPTS = ["order_date"]
CATEGORY_CONCEPTS = ["category", "sub_category"]
PRODUCT_CONCEPTS = ["product_name", "product_id"]
GEO_CONCEPTS = ["region", "country", "market"]
SEGMENT_CONCEPTS = ["segment"]


# ──────────────────────────────────────────────────────────────────────────────
# Workspace registry — in-memory store
# ──────────────────────────────────────────────────────────────────────────────
import os
from backend.app.db.database import SessionLocal, engine, Base
from backend.app.db.models import Workspace

Base.metadata.create_all(bind=engine)

class DBWorkspaceRegistry:
    """Persistent workspace store using SQLAlchemy and local Parquet files."""
    
    def __init__(self):
        self.upload_dir = "/tmp/uploads"
        os.makedirs(self.upload_dir, exist_ok=True)

    def create(self, dataset_id: str, filename: str, df: pd.DataFrame, user_id: str = "legacy_user") -> Dict:
        object_key = storage_service.save_dataframe(df, user_id, dataset_id)
        
        profile_data = {
            "row_count": len(df),
            "column_count": len(df.columns),
        }
        
        db = SessionLocal()
        try:
            ws_model = Workspace(
                id=dataset_id,
                user_id=user_id,
                filename=filename,
                filepath=object_key,
                status="uploaded",
                mapping={},
                profile=profile_data,
            )
            db.add(ws_model)
            db.commit()
            logger.info(f"Workspace created in DB: {dataset_id} ({filename}, {len(df)} rows)")
        finally:
            db.close()
            
        return self._public({
            "dataset_id": dataset_id,
            "filename": filename,
            "status": "uploaded",
            "row_count": len(df),
            "column_count": len(df.columns)
        })

    def get(self, dataset_id: str, user_id: str = None) -> Optional[Dict]:
        db = SessionLocal()
        try:
            query = db.query(Workspace).filter(Workspace.id == dataset_id)
            if user_id:
                query = query.filter(Workspace.user_id == user_id)
            ws_model = query.first()
            if not ws_model:
                return None
            
            # Reconstruct the dict
            ws = {
                "dataset_id": ws_model.id,
                "filename": ws_model.filename,
                "status": ws_model.status,
                "created_at": ws_model.created_at.isoformat(),
                "mapping": ws_model.mapping or {},
                "dashboard": ws_model.dashboard,
                "insights": ws_model.insights,
                "recommendations": ws_model.recommendations,
                "filepath": ws_model.filepath,
            }
            # Merge profile
            if ws_model.profile:
                for k, v in ws_model.profile.items():
                    if k not in ws and k not in ("mapping", "status", "filename", "dataset_id"):
                        ws[k] = v
                
            # Load DataFrame lazily when requested?
            # Existing code expects `ws["df"]` to be available. We'll load it here.
            try:
                df_loaded = storage_service.load_dataframe(ws_model.filepath)
                if ws_model.mapping:
                    numeric_concepts = ["sales", "profit", "discount", "quantity", "shipping_cost"]
                    m = ws_model.mapping
                    for concept in numeric_concepts:
                        c = m.get(concept)
                        if c and c in df_loaded.columns and not pd.api.types.is_numeric_dtype(df_loaded[c]):
                            df_loaded[c] = pd.to_numeric(df_loaded[c].astype(str).str.replace(r'[^\d\.\-]', '', regex=True), errors='coerce').fillna(0.0)
                ws["df"] = df_loaded
            except Exception as e:
                logger.error(f"Failed to load dataset file for {dataset_id}: {e}")
                ws["df"] = pd.DataFrame()
                
            return ws
        finally:
            db.close()

    def list(self, user_id: str = None) -> List[Dict]:
        db = SessionLocal()
        try:
            query = db.query(Workspace)
            if user_id:
                query = query.filter(Workspace.user_id == user_id)
            workspaces = query.all()
            results = []
            for ws_model in workspaces:
                ws = {
                    "dataset_id": ws_model.id,
                    "filename": ws_model.filename,
                    "status": ws_model.status,
                    "created_at": ws_model.created_at.isoformat(),
                }
                if ws_model.profile:
                    for k, v in ws_model.profile.items():
                        if k not in ws:
                            ws[k] = v
                results.append(self._public(ws))
            return results
        finally:
            db.close()

    def update(self, dataset_id: str, user_id: str = None, **kwargs):
        db = SessionLocal()
        try:
            query = db.query(Workspace).filter(Workspace.id == dataset_id)
            if user_id:
                query = query.filter(Workspace.user_id == user_id)
            ws_model = query.first()
            if ws_model:

                # If df is in kwargs, we need to save it to disk! (because compute_dashboard mutates it)
                if "df" in kwargs:
                    df = kwargs.pop("df")
                    from backend.app.services.storage_service import storage_service
                    # We save it using storage_service
                    ws_model.filepath = storage_service.save_dataframe(df, ws_model.user_id, ws_model.id)

                
                if "mapping" in kwargs:
                    ws_model.mapping = kwargs.pop("mapping")
                if "dashboard" in kwargs:
                    ws_model.dashboard = kwargs.pop("dashboard")
                if "insights" in kwargs:
                    ws_model.insights = kwargs.pop("insights")
                if "recommendations" in kwargs:
                    ws_model.recommendations = kwargs.pop("recommendations")
                if "status" in kwargs:
                    ws_model.status = kwargs.pop("status")
                
                # Any other kwargs go to profile
                if kwargs:
                    prof = dict(ws_model.profile) if ws_model.profile else {}
                    prof.update(kwargs)
                    ws_model.profile = prof
                    
                db.commit()
        finally:
            db.close()

    def delete(self, dataset_id: str, user_id: str = None):
        db = SessionLocal()
        try:
            query = db.query(Workspace).filter(Workspace.id == dataset_id)
            if user_id:
                query = query.filter(Workspace.user_id == user_id)
            ws_model = query.first()
            if ws_model:
                storage_service.delete_object(ws_model.filepath)
                db.delete(ws_model)
                db.commit()
        finally:
            db.close()

    def _public(self, ws: Dict) -> Dict:
        return {k: v for k, v in ws.items() if k not in ("df", "filepath")}

workspace_registry = DBWorkspaceRegistry()


# ──────────────────────────────────────────────────────────────────────────────
# File loading
# ──────────────────────────────────────────────────────────────────────────────
def load_file(content: bytes, filename: str) -> pd.DataFrame:
    """Safely load CSV or XLSX from bytes. Returns cleaned DataFrame."""
    fn_lower = filename.lower()
    try:
        if fn_lower.endswith(".csv"):
            # Try utf-8 first, fall back to latin-1
            try:
                df = pd.read_csv(io.BytesIO(content), encoding="utf-8")
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding="latin-1")
        elif fn_lower.endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise ValueError(f"Unsupported file type: {filename}. Use CSV or XLSX.")
    except Exception as e:
        raise ValueError(f"Could not read file: {e}")

    if df.empty:
        raise ValueError("Uploaded file contains no data rows.")
    if len(df.columns) < 2:
        raise ValueError("File must have at least 2 columns.")

    # Normalize column names: strip whitespace, lowercase
    df.columns = [str(c).strip() for c in df.columns]

    # Replace inf/-inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    return df


# ──────────────────────────────────────────────────────────────────────────────
# Column profiling and auto-mapping
# ──────────────────────────────────────────────────────────────────────────────
def profile_columns(df: pd.DataFrame) -> Dict:
    """Detect column roles and auto-suggest business concept mappings."""
    col_lower = {c.lower().replace(" ", "_"): c for c in df.columns}
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    date_cols = []
    categorical_cols = []

    for c in df.columns:
        if c in numeric_cols:
            continue
        # Try parsing as date
        sample = df[c].dropna().head(20)
        parsed = pd.to_datetime(sample, errors="coerce")
        if parsed.notna().sum() >= min(5, len(sample)):
            date_cols.append(c)
        else:
            categorical_cols.append(c)

    # Auto-suggest mappings
    suggested: Dict[str, str] = {}
    used_sources = set()

    for concept, hints in CONCEPT_HINTS.items():
        # Exact match
        for hint in hints:
            if hint in col_lower and col_lower[hint] not in used_sources:
                suggested[concept] = col_lower[hint]
                used_sources.add(col_lower[hint])
                break
        
        # If not exact match, do a conservative partial match
        if concept not in suggested:
            for hint in hints:
                if len(hint) < 4:
                    continue  # Too short for partial match
                for raw_lower, raw_orig in col_lower.items():
                    if raw_orig in used_sources:
                        continue
                    # Check for whole word match within the string or start/end
                    import re
                    pattern = rf"(^|_|){re.escape(hint)}(_||$)"
                    if re.search(pattern, raw_lower) and raw_orig not in used_sources:
                        suggested[concept] = raw_orig
                        used_sources.add(raw_orig)
                        break
                if concept in suggested:
                    break

    # Determine which analytics modules are available
    available_modules = _determine_modules(suggested, df)

    return {
        "columns": list(df.columns),
        "numeric_columns": numeric_cols,
        "date_columns": date_cols,
        "categorical_columns": categorical_cols,
        "suggested_mapping": suggested,
        "available_modules": available_modules,
    }


def _determine_modules(mapping: Dict[str, str], df: pd.DataFrame) -> Dict[str, bool]:
    has = lambda c: c in mapping and mapping[c] in df.columns
    return {
        "total_sales":         has("sales"),
        "sales_trend":         has("sales") and has("order_date"),
        "category_breakdown":  has("sales") and (has("category") or has("sub_category")),
        "product_performance": has("sales") and (has("product_name") or has("product_id")),
        "profitability":       has("profit") and has("sales"),
        "geographic":          has("sales") and (has("region") or has("country") or has("market")),
        "segment_analysis":    has("sales") and has("segment"),
        "discount_analysis":   has("discount") and has("profit"),
        "order_analysis":      has("order_id") and has("sales"),
        "recommendations":     has("sales"),
        "insights":            has("sales"),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Data quality profiling
# ──────────────────────────────────────────────────────────────────────────────
def compute_quality(df: pd.DataFrame) -> Dict:
    missing = df.isnull().sum().to_dict()
    missing_pct = {k: round(v / len(df) * 100, 2) for k, v in missing.items()}
    dupe_count = int(df.duplicated().sum())

    warnings = []
    if dupe_count > 0:
        warnings.append(f"{dupe_count} duplicate rows detected.")
    high_missing = [c for c, pct in missing_pct.items() if pct > 30]
    if high_missing:
        warnings.append(f"High missing values (>30%) in: {', '.join(high_missing[:5])}")

    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": dupe_count,
        "missing_counts": {k: int(v) for k, v in missing.items()},
        "missing_pct": missing_pct,
        "warnings": warnings,
        "quality_score": "High" if dupe_count < 100 and not high_missing else "Medium",
    }


# ──────────────────────────────────────────────────────────────────────────────
# Dashboard analytics — conditional on confirmed mapping
# ──────────────────────────────────────────────────────────────────────────────
def compute_dashboard(df: pd.DataFrame, mapping: Dict[str, str]) -> Dict:
    """Compute all available analytics for the workspace dashboard."""
    m = mapping  # shorthand
    result = {"modules": {}, "available": {}}

    # Helper: get actual column name from mapping
    def col(concept: str) -> Optional[str]:
        c = m.get(concept)
        return c if c and c in df.columns else None

    # Force coerce numeric columns to prevent string concatenation sums (e.g. string to float errors)
    numeric_concepts = ["sales", "profit", "discount", "quantity", "shipping_cost"]
    for concept in numeric_concepts:
        c = col(concept)
        if c and not pd.api.types.is_numeric_dtype(df[c]):
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'[^\d\.\-]', '', regex=True), errors='coerce').fillna(0.0)

    # ── KPIs ──
    kpis = []
    if col("sales"):
        total_sales = float(df[col("sales")].sum())
        kpis.append({"label": "Total Sales", "value": f"${total_sales:,.2f}", "raw": total_sales})
    if col("profit"):
        total_profit = float(df[col("profit")].sum())
        kpis.append({"label": "Total Profit", "value": f"${total_profit:,.2f}", "raw": total_profit})
    if col("sales") and col("profit"):
        ts = float(df[col("sales")].sum())
        tp = float(df[col("profit")].sum())
        margin = (tp / ts * 100) if ts else 0
        kpis.append({"label": "Profit Margin", "value": f"{margin:.2f}%", "raw": margin})
    if col("order_id"):
        unique_orders = int(df[col("order_id")].nunique())
        kpis.append({"label": "Unique Orders", "value": f"{unique_orders:,}", "raw": unique_orders})
    if col("quantity"):
        total_qty = int(df[col("quantity")].sum())
        kpis.append({"label": "Total Quantity", "value": f"{total_qty:,}", "raw": total_qty})
    if col("discount"):
        avg_disc = float(df[col("discount")].mean()) * 100
        kpis.append({"label": "Avg Discount", "value": f"{avg_disc:.2f}%", "raw": avg_disc})
    result["kpis"] = kpis
    
    # ── ML Predictions ──
    ml_status = prediction_service.check_compatibility(mapping)
    result["ml_compatibility"] = ml_status
    if ml_status.get("compatible"):
        try:
            preds = prediction_service.predict_batch(df, mapping)
            total_pred_profit = float(preds.sum())
            kpis.append({"label": "Predicted Profit (ML)", "value": f"${total_pred_profit:,.2f}", "raw": total_pred_profit, "is_ml": True})
            
            # Aggregate predictions by Category if available
            if col("category"):
                df_temp = df.copy()
                df_temp["_pred_profit"] = preds
                cat_preds = df_temp.groupby(col("category"))["_pred_profit"].sum().reset_index()
                cat_preds = cat_preds.sort_values("_pred_profit", ascending=False).to_dict("records")
                result["ml_predictions_by_category"] = [
                    {"category": row[col("category")], "predicted_profit": row["_pred_profit"]} 
                    for row in cat_preds
                ]
            result["ml_predictions"] = {"total_predicted_profit": total_pred_profit, "model_info": prediction_service.get_model_info()}
        except Exception as e:
            logger.error(f"Failed to generate ML predictions for dashboard: {e}")
            result["ml_compatibility"]["error"] = str(e)
            result["ml_compatibility"]["compatible"] = False

    # ── Sales Trend ──
    if col("sales") and col("order_date"):
        dft = df[[col("sales"), col("order_date")]].copy()
        dft[col("order_date")] = pd.to_datetime(dft[col("order_date")], errors="coerce")
        dft = dft.dropna(subset=[col("order_date")])
        if not dft.empty:
            dft["_period"] = dft[col("order_date")].dt.to_period("M")
            trend = dft.groupby("_period").agg(sales=(col("sales"), "sum")).reset_index()
            trend["_period"] = trend["_period"].astype(str)
            profit_col = col("profit")
            if profit_col:
                dft2 = df[[col("sales"), col("order_date"), profit_col]].copy()
                dft2[col("order_date")] = pd.to_datetime(dft2[col("order_date")], errors="coerce")
                dft2 = dft2.dropna(subset=[col("order_date")])
                dft2["_period"] = dft2[col("order_date")].dt.to_period("M")
                profit_trend = dft2.groupby("_period").agg(profit=(profit_col, "sum")).reset_index()
                profit_trend["_period"] = profit_trend["_period"].astype(str)
                trend = trend.merge(profit_trend[["_period", "profit"]], on="_period", how="left")
                trend = trend.rename(columns={"_period": "period"})
            else:
                trend = trend.rename(columns={"_period": "period"})
            result["sales_trend"] = _safe_records(trend)
        else:
            result["sales_trend"] = []
    else:
        result["sales_trend"] = None  # unavailable

    # ── Category Breakdown ──
    cat_col = col("category") or col("sub_category")
    if col("sales") and cat_col:
        cat_df = df.groupby(cat_col).agg(value=(col("sales"), "sum")).reset_index()
        cat_df = cat_df.rename(columns={cat_col: "name"})
        cat_df = cat_df.sort_values("value", ascending=False).head(10)
        if col("profit"):
            p = df.groupby(cat_col).agg(profit=(col("profit"), "sum")).reset_index()
            p = p.rename(columns={cat_col: "name"})
            cat_df = cat_df.merge(p, on="name", how="left")
        result["category_breakdown"] = _safe_records(cat_df)
    else:
        result["category_breakdown"] = None

    # ── Product Performance ──
    prod_col = col("product_name") or col("product_id")
    if col("sales") and prod_col:
        prod_df = df.groupby(prod_col).agg(sales=(col("sales"), "sum")).reset_index()
        prod_df = prod_df.rename(columns={prod_col: "name"})
        prod_df = prod_df.sort_values("sales", ascending=False).head(15)
        if col("profit"):
            pp = df.groupby(prod_col).agg(profit=(col("profit"), "sum")).reset_index()
            pp = pp.rename(columns={prod_col: "name"})
            prod_df = prod_df.merge(pp, on="name", how="left")
        result["product_performance"] = _safe_records(prod_df)
    else:
        result["product_performance"] = None

    # ── Geographic Summary ──
    geo_col = col("region") or col("country") or col("market")
    if col("sales") and geo_col:
        geo_df = df.groupby(geo_col).agg(sales=(col("sales"), "sum")).reset_index()
        geo_df = geo_df.rename(columns={geo_col: "name"})
        geo_df = geo_df.sort_values("sales", ascending=False)
        if col("profit"):
            gp = df.groupby(geo_col).agg(profit=(col("profit"), "sum")).reset_index()
            gp = gp.rename(columns={geo_col: "name"})
            geo_df = geo_df.merge(gp, on="name", how="left")
        result["geographic"] = _safe_records(geo_df)
    else:
        result["geographic"] = None

    # ── Segment Analysis ──
    if col("sales") and col("segment"):
        seg_df = df.groupby(col("segment")).agg(sales=(col("sales"), "sum")).reset_index()
        seg_df = seg_df.rename(columns={col("segment"): "name"})
        if col("profit"):
            sp = df.groupby(col("segment")).agg(profit=(col("profit"), "sum")).reset_index()
            sp = sp.rename(columns={col("segment"): "name"})
            seg_df = seg_df.merge(sp, on="name", how="left")
        result["segment"] = _safe_records(seg_df)
    else:
        result["segment"] = None

    # ── Profitability Quadrant ──
    if col("sales") and col("profit") and (cat_col or prod_col):
        dim_col = cat_col or prod_col
        pq = df.groupby(dim_col).agg(
            sales=(col("sales"), "sum"),
            profit=(col("profit"), "sum")
        ).reset_index()
        pq["margin"] = np.where(pq["sales"] > 0, pq["profit"] / pq["sales"] * 100, 0)
        pq = pq.rename(columns={dim_col: "name"})
        result["profitability_quadrant"] = _safe_records(pq.head(20))
    else:
        result["profitability_quadrant"] = None

    # ── Available modules flags ──
    result["available_modules"] = _determine_modules(mapping, df)
    result["dataset_label"] = "Workspace Data"

    return result


def _safe_records(df: pd.DataFrame) -> List[Dict]:
    """Convert DataFrame to JSON-safe records."""
    records = []
    for row in df.to_dict("records"):
        safe = {}
        for k, v in row.items():
            if pd.isna(v) if not isinstance(v, (list, dict)) else False:
                safe[k] = None
            elif isinstance(v, (np.integer,)):
                safe[k] = int(v)
            elif isinstance(v, (np.floating,)):
                safe[k] = float(v) if not np.isinf(v) else None
            else:
                safe[k] = v
        records.append(safe)
    return records


# ──────────────────────────────────────────────────────────────────────────────
# Insights engine
# ──────────────────────────────────────────────────────────────────────────────
def compute_insights(df: pd.DataFrame, mapping: Dict[str, str], dataset_id: str) -> List[Dict]:
    m = mapping
    insights = []
    ts = datetime.utcnow().isoformat()

    def col(c): return m.get(c) if m.get(c) and m.get(c) in df.columns else None

    # ── Time Series Insights ──
    if col("sales") and col("order_date"):
        try:
            dft = df[[col("sales"), col("order_date")]].copy()
            dft[col("order_date")] = pd.to_datetime(dft[col("order_date")], errors="coerce")
            dft = dft.dropna(subset=[col("order_date")])
            if not dft.empty:
                dft["_period"] = dft[col("order_date")].dt.to_period("M")
                trend = dft.groupby("_period")[col("sales")].sum()
                if len(trend) >= 2:
                    best_month = trend.idxmax()
                    best_sales = float(trend.max())
                    insights.append({
                        "id": f"{dataset_id}_best_month",
                        "type": "Analytical Insight",
                        "title": f"Peak Revenue: {best_month}",
                        "description": f"The highest sales period was {best_month}, generating ${best_sales:,.0f} in revenue.",
                        "affected_entity": str(best_month),
                        "evidence": {"best_month": str(best_month), "sales_volume": best_sales},
                        "method": "Monthly aggregation, maximum value",
                        "generated_at": ts,
                    })
        except Exception:
            pass

    # ── Top category by sales ──
    cat_col = col("category") or col("sub_category")
    if col("sales") and cat_col:
        cat_sales = df.groupby(cat_col)[col("sales")].sum()
        top_cat = cat_sales.idxmax()
        top_val = float(cat_sales.max())
        total_val = float(cat_sales.sum())
        share = top_val / total_val * 100 if total_val else 0
        insights.append({
            "id": f"{dataset_id}_top_cat",
            "type": "Analytical Insight",
            "title": f"Top Category: {top_cat}",
            "description": f"{top_cat} generated the largest revenue share ({share:.1f}%) with ${top_val:,.0f} in total sales.",
            "affected_entity": str(top_cat),
            "evidence": {"top_sales": top_val, "share_pct": round(share, 2), "total_sales": total_val},
            "method": "Sum by category, highest value",
            "generated_at": ts,
        })

    # ── Low-margin high-sales products ──
    prod_col = col("product_name") or col("product_id")
    if col("sales") and col("profit") and prod_col:
        prod = df.groupby(prod_col).agg(
            sales=(col("sales"), "sum"), profit=(col("profit"), "sum")
        ).reset_index()
        prod["margin"] = np.where(prod["sales"] > 0, prod["profit"] / prod["sales"], 0)
        median_sales = prod["sales"].median()
        weak = prod[(prod["sales"] > median_sales) & (prod["margin"] < 0.05)]
        if not weak.empty:
            count = len(weak)
            insights.append({
                "id": f"{dataset_id}_low_margin_prods",
                "type": "Risk Alert",
                "title": f"{count} High-Revenue, Low-Margin Products",
                "description": f"{count} product(s) generate above-median revenue but achieve less than 5% margin. These may be eroding overall profitability.",
                "affected_entity": str(weak[prod_col].iloc[0]) if count == 1 else f"{count} products",
                "evidence": {
                    "count": count,
                    "threshold_margin": "5%",
                    "sample": str(weak[prod_col].iloc[0]),
                    "sample_margin": round(float(weak["margin"].iloc[0]) * 100, 2),
                },
                "method": "Products with sales > median AND margin < 5%",
                "generated_at": ts,
            })

    # ── Discount-profit relationship ──
    if col("discount") and col("profit") and col("sales"):
        high_disc = df[df[col("discount")] > 0.2]
        if len(high_disc) > 0:
            disc_margin = float(high_disc[col("profit")].sum()) / float(high_disc[col("sales")].sum()) * 100 if float(high_disc[col("sales")].sum()) else 0
            all_margin = float(df[col("profit")].sum()) / float(df[col("sales")].sum()) * 100 if float(df[col("sales")].sum()) else 0
            if disc_margin < all_margin - 3:
                insights.append({
                    "id": f"{dataset_id}_discount_drag",
                    "type": "Risk Alert",
                    "title": "High Discounts Compress Margins",
                    "description": f"Orders with >20% discount achieve {disc_margin:.1f}% margin, vs. {all_margin:.1f}% overall. High discounting appears to drag profitability.",
                    "affected_entity": "Discounted orders",
                    "evidence": {
                        "high_discount_margin_pct": round(disc_margin, 2),
                        "overall_margin_pct": round(all_margin, 2),
                        "high_discount_order_count": len(high_disc),
                    },
                    "method": "Compare average margin for discount > 20% vs. all orders",
                    "generated_at": ts,
                })

    # ── Loss-making categories ──
    if col("profit") and cat_col:
        cat_profit = df.groupby(cat_col)[col("profit")].sum()
        loss_cats = cat_profit[cat_profit < 0]
        for cat, pval in loss_cats.items():
            insights.append({
                "id": f"{dataset_id}_loss_{cat}",
                "type": "Risk Alert",
                "title": f"Loss-Making: {cat}",
                "description": f"{cat} has accumulated ${abs(pval):,.0f} in net losses. Consider investigating root causes.",
                "affected_entity": str(cat),
                "evidence": {"total_profit": round(float(pval), 2)},
                "method": "Sum profit by category, identify negative values",
                "generated_at": ts,
            })

    # ── Geographic margin variance ──
    geo_col = col("region") or col("country") or col("market")
    if col("sales") and col("profit") and geo_col:
        geo = df.groupby(geo_col).agg(sales=(col("sales"), "sum"), profit=(col("profit"), "sum")).reset_index()
        geo["margin"] = np.where(geo["sales"] > 0, geo["profit"] / geo["sales"] * 100, 0)
        if len(geo) >= 2:
            best = geo.loc[geo["margin"].idxmax()]
            worst = geo.loc[geo["margin"].idxmin()]
            if float(best["margin"]) - float(worst["margin"]) > 5:
                insights.append({
                    "id": f"{dataset_id}_geo_variance",
                    "type": "Analytical Insight",
                    "title": "Significant Margin Variance Across Regions",
                    "description": f"{best[geo_col]} leads with {best['margin']:.1f}% margin; {worst[geo_col]} lags at {worst['margin']:.1f}%. A {best['margin']-worst['margin']:.1f} percentage point gap may indicate regional pricing or cost differences.",
                    "affected_entity": f"{best[geo_col]} vs {worst[geo_col]}",
                    "evidence": {
                        "best_region": str(best[geo_col]),
                        "best_margin_pct": round(float(best["margin"]), 2),
                        "worst_region": str(worst[geo_col]),
                        "worst_margin_pct": round(float(worst["margin"]), 2),
                    },
                    "method": "Group by geographic dimension, compare profit margin",
                    "generated_at": ts,
                })

    # ── Revenue concentration ──
    if col("sales") and prod_col:
        prod_s = df.groupby(prod_col)[col("sales")].sum().sort_values(ascending=False)
        top5_share = prod_s.head(5).sum() / prod_s.sum() * 100 if prod_s.sum() else 0
        if top5_share > 50:
            insights.append({
                "id": f"{dataset_id}_concentration",
                "type": "Analytical Insight",
                "title": "High Revenue Concentration in Top Products",
                "description": f"The top 5 products account for {top5_share:.1f}% of total sales. High concentration increases business risk if any of those products underperform.",
                "affected_entity": "Top 5 products",
                "evidence": {"top5_share_pct": round(top5_share, 2), "total_products": int(len(prod_s))},
                "method": "Top-5 products share of total sales",
                "generated_at": ts,
            })

    # ── Fallback ──
    if not insights and col("sales"):
        sales_sum = float(df[col("sales")].sum())
        insights.append({
            "id": f"{dataset_id}_general_summary",
            "type": "Analytical Insight",
            "title": "Baseline Performance Active",
            "description": f"The dataset has been successfully processed, identifying ${sales_sum:,.0f} in total mapped volume. Map additional columns like Profit, Category, or Region to unlock deeper strategic insights.",
            "affected_entity": "Entire Dataset",
            "evidence": {"total_volume": sales_sum},
            "method": "Baseline Aggregation",
            "generated_at": ts,
        })
        
    return insights


# ──────────────────────────────────────────────────────────────────────────────
# Recommendations engine — uses existing RecommendationService pattern
# ──────────────────────────────────────────────────────────────────────────────
def compute_recommendations(df: pd.DataFrame, mapping: Dict[str, str], dataset_id: str) -> List[Dict]:
    """Generate evidence-backed business recommendations from workspace data."""
    from backend.app.services.recommendation_service import recommendation_service

    # Rename columns to standard names that recommendation_service understands
    rename = {v: k for k, v in mapping.items() if v in df.columns}
    df_std = df.rename(columns=rename)

    # Add mapped aliases expected by recommendation_service
    if "product_id" not in df_std.columns and "product_name" in df_std.columns:
        df_std["product_id"] = df_std["product_name"]
    if "sub_category" not in df_std.columns and "category" in df_std.columns:
        df_std["sub_category"] = df_std["category"]

    recs = recommendation_service.generate_recommendations(df_std)

    # Tag each recommendation with workspace context
    for r in recs:
        r["dataset_id"] = dataset_id
        r["source"] = "workspace_rule_engine"

    return recs


# ──────────────────────────────────────────────────────────────────────────────
# Validation helpers
# ──────────────────────────────────────────────────────────────────────────────
def validate_mapping(df: pd.DataFrame, mapping: Dict[str, str]) -> Dict:
    """Check which analytics are available, warn about missing fields."""
    errors = []
    warnings = []
    info = []

    # Check for missing columns, duplicates, and type compatibility
    import pandas as pd
    from backend.app.services.storage_service import storage_service
    seen_cols = {}
    
    # Define expected numeric concepts
    numeric_concepts = {"sales", "profit", "discount", "quantity", "shipping_cost"}
    date_concepts = {"order_date", "ship_date"}

    for concept, col_name in mapping.items():
        if not col_name:
            continue
        if col_name not in df.columns:
            errors.append(f"Mapped column '{col_name}' for '{concept}' not found in dataset.")
        else:
            if col_name in seen_cols:
                errors.append(f"Source column '{col_name}' is mapped multiple times (to '{seen_cols[col_name]}' and '{concept}').")
            else:
                seen_cols[col_name] = concept
            
            # Type validation
            if concept in numeric_concepts:
                if not pd.api.types.is_numeric_dtype(df[col_name]):
                    # Check if it can be coerced
                    coerced = pd.to_numeric(df[col_name].astype(str).str.replace(r'[^\d\.\-]', '', regex=True), errors='coerce')
                    if coerced.isna().sum() > len(df) * 0.5:
                        errors.append(f"Column '{col_name}' mapped to '{concept}' contains too many non-numeric values.")
            
            if concept in date_concepts:
                if not pd.api.types.is_datetime64_any_dtype(df[col_name]):
                    coerced = pd.to_datetime(df[col_name], errors='coerce')
                    if coerced.isna().sum() > len(df) * 0.5:
                        errors.append(f"Column '{col_name}' mapped to '{concept}' contains too many invalid dates.")


    has = lambda c: c in mapping and mapping.get(c, "") in df.columns

    if not has("sales"):
        warnings.append("No 'sales' column mapped — most analytics unavailable.")
    if not has("order_date"):
        info.append("No date column mapped — time-trend charts will be unavailable.")
    if not has("profit"):
        info.append("No profit column — profitability and margin analysis unavailable.")
    if not has("category") and not has("sub_category"):
        info.append("No category column — category breakdowns unavailable.")
    if not has("region") and not has("country") and not has("market"):
        info.append("No geographic column — regional analysis unavailable.")

    modules = _determine_modules(mapping, df)
    available_count = sum(1 for v in modules.values() if v)

    return {
        "errors": errors,
        "warnings": warnings,
        "info": info,
        "available_modules": modules,
        "available_count": available_count,
        "valid": len(errors) == 0,
    }
