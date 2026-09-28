"""
SalesBrain Navigator — Dataset/Workspace API Routes
Handles user-uploaded dataset lifecycle for My Data Workspace.
"""

import uuid
import io
import csv
import json
import logging
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.app.services.workspace_service import (
    workspace_registry,
    load_file,
    profile_columns,
    compute_quality,
    compute_dashboard,
    compute_insights,
    compute_recommendations,
    validate_mapping,
)

logger = logging.getLogger("SalesBrain")
router = APIRouter()

# ── Constants ──────────────────────────────────────────────────────────────
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
PREVIEW_ROWS = 50


# ── Request / Response Models ─────────────────────────────────────────────

class ColumnMappingRequest(BaseModel):
    mapping: Dict[str, str]  # concept → column_name


class CreateDashboardRequest(BaseModel):
    mapping: Dict[str, str]


class WorkspaceMeta(BaseModel):
    dataset_id: str
    filename: str
    created_at: str
    row_count: int
    column_count: int
    status: str


# ── Upload ────────────────────────────────────────────────────────────────

@router.post("/datasets/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a retail CSV or XLSX file and create a new workspace.
    Returns dataset_id, profile, and quality summary.
    """
    # Validate extension
    filename = file.filename or "upload"
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Please upload a CSV or XLSX file."
        )

    # Read content
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(content)/(1024*1024):.1f}MB). Maximum is {MAX_FILE_SIZE_MB}MB."
        )

    # Load into DataFrame
    try:
        df = load_file(content, filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error loading uploaded file: {e}")
        raise HTTPException(status_code=500, detail=f"Could not process file: {e}")

    # Generate workspace
    dataset_id = str(uuid.uuid4())
    workspace_registry.create(dataset_id, filename, df)

    # Profile and quality
    profile = profile_columns(df)
    quality = compute_quality(df)
    workspace_registry.update(dataset_id, profile=profile, quality=quality, status="profiled")

    return {
        "dataset_id": dataset_id,
        "filename": filename,
        "row_count": len(df),
        "column_count": len(df.columns),
        "profile": profile,
        "quality": quality,
        "message": "Dataset uploaded and profiled successfully.",
    }


# ── List workspaces ────────────────────────────────────────────────────────

@router.get("/datasets")
def list_datasets():
    return {"datasets": workspace_registry.list()}


# ── Get workspace metadata ─────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return workspace_registry._public(ws)


# ── Preview rows ───────────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/preview")
def get_dataset_preview(dataset_id: str, rows: int = Query(default=50, le=200)):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    df = ws["df"]
    sample = df.head(rows)

    records = []
    for row in sample.to_dict("records"):
        safe = {}
        for k, v in row.items():
            import numpy as np, pandas as pd
            if isinstance(v, float) and (pd.isna(v) or not pd.notnull(v)):
                safe[k] = None
            elif isinstance(v, (int, float, str, bool, type(None))):
                safe[k] = v
            else:
                safe[k] = str(v)
        records.append(safe)

    return {
        "dataset_id": dataset_id,
        "total_rows": len(df),
        "preview_rows": len(records),
        "columns": list(df.columns),
        "records": records,
    }


# ── Schema / profile ────────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/schema")
def get_dataset_schema(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {
        "dataset_id": dataset_id,
        "profile": ws.get("profile", {}),
    }


# ── Quality report ──────────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/quality")
def get_dataset_quality(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    return {"dataset_id": dataset_id, "quality": ws.get("quality", {})}


# ── Map columns ─────────────────────────────────────────────────────────────

@router.post("/datasets/{dataset_id}/map-columns")
def map_columns(dataset_id: str, body: ColumnMappingRequest):
    """Confirm column mapping and validate which analytics are available."""
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    df = ws["df"]

    validation = validate_mapping(df, body.mapping)
    if not validation["valid"]:
        raise HTTPException(status_code=422, detail=" | ".join(validation["errors"]))

    workspace_registry.update(dataset_id, mapping=body.mapping, status="mapped")

    return {
        "dataset_id": dataset_id,
        "mapping": body.mapping,
        "validation": validation,
        "message": "Column mapping confirmed.",
    }


# ── Create / generate dashboard ─────────────────────────────────────────────

@router.post("/datasets/{dataset_id}/create-dashboard")
def create_dashboard(dataset_id: str, body: Optional[CreateDashboardRequest] = None):
    """
    Compute analytics from the uploaded dataset and store the dashboard.
    Uses the mapping from body (if provided) or the previously confirmed mapping.
    """
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    df = ws["df"]

    mapping = (body.mapping if body else None) or ws.get("mapping") or {}
    if not mapping:
        raise HTTPException(
            status_code=400,
            detail="No column mapping available. Please map columns first."
        )

    try:
        dashboard = compute_dashboard(df, mapping)
    except Exception as e:
        logger.error(f"Dashboard computation error for {dataset_id}: {e}")
        raise HTTPException(status_code=422, detail=f"Analytics computation failed: {e}")

    workspace_registry.update(
        dataset_id,
        mapping=mapping,
        dashboard=dashboard,
        status="dashboard_ready"
    )

    return {
        "dataset_id": dataset_id,
        "status": "dashboard_ready",
        "dashboard": dashboard,
        "message": "Dashboard created from your data.",
    }


# ── Get dashboard ────────────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/dashboard")
def get_dashboard(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    dashboard = ws.get("dashboard")
    if not dashboard:
        raise HTTPException(
            status_code=400,
            detail="Dashboard not yet created. Call POST /create-dashboard first."
        )
    return {"dataset_id": dataset_id, "dashboard": dashboard}


# ── Generate insights ───────────────────────────────────────────────────────

@router.post("/datasets/{dataset_id}/generate-insights")
def generate_insights(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    df = ws["df"]
    mapping = ws.get("mapping", {})
    if not mapping:
        raise HTTPException(status_code=400, detail="Map columns before generating insights.")

    try:
        insights = compute_insights(df, mapping, dataset_id)
    except Exception as e:
        logger.error(f"Insight generation error for {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Insight generation failed: {e}")

    workspace_registry.update(dataset_id, insights=insights)

    return {
        "dataset_id": dataset_id,
        "count": len(insights),
        "insights": insights,
        "message": f"{len(insights)} insights generated from your dataset.",
    }


# ── Get cached insights ─────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/insights")
def get_insights(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    insights = ws.get("insights")
    if insights is None:
        raise HTTPException(status_code=400, detail="Insights not yet generated.")
    return {"dataset_id": dataset_id, "count": len(insights), "insights": insights}


# ── Generate recommendations ─────────────────────────────────────────────────

@router.post("/datasets/{dataset_id}/generate-recommendations")
def generate_recommendations(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    df = ws["df"]
    mapping = ws.get("mapping", {})
    if not mapping:
        raise HTTPException(status_code=400, detail="Map columns before generating recommendations.")

    try:
        recs = compute_recommendations(df, mapping, dataset_id)
    except Exception as e:
        logger.error(f"Recommendation error for {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Recommendation generation failed: {e}")

    workspace_registry.update(dataset_id, recommendations=recs)

    return {
        "dataset_id": dataset_id,
        "count": len(recs),
        "recommendations": recs,
        "message": f"{len(recs)} recommendations generated.",
    }


# ── Get cached recommendations ──────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/recommendations")
def get_recommendations(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    recs = ws.get("recommendations")
    if recs is None:
        raise HTTPException(status_code=400, detail="Recommendations not yet generated.")
    return {"dataset_id": dataset_id, "count": len(recs), "recommendations": recs}


# ── Export ─────────────────────────────────────────────────────────────────

@router.get("/datasets/{dataset_id}/export")
def export_dataset_report(dataset_id: str, report_type: str = Query(default="kpis")):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    dashboard = ws.get("dashboard", {})
    insights = ws.get("insights", [])
    recommendations = ws.get("recommendations", [])
    filename_base = ws.get("filename", "workspace").rsplit(".", 1)[0]

    stream = io.StringIO()

    if report_type == "insights":
        writer = csv.DictWriter(stream, fieldnames=["id", "type", "title", "description", "affected_entity", "generated_at"])
        writer.writeheader()
        for ins in insights:
            writer.writerow({
                "id": ins.get("id", ""),
                "type": ins.get("type", ""),
                "title": ins.get("title", ""),
                "description": ins.get("description", ""),
                "affected_entity": ins.get("affected_entity", ""),
                "generated_at": ins.get("generated_at", ""),
            })
        dl_name = f"{filename_base}_insights.csv"

    elif report_type == "recommendations":
        writer = csv.DictWriter(stream, fieldnames=["id", "title", "insight", "affected_entity", "priority", "suggested_action"])
        writer.writeheader()
        for rec in recommendations:
            writer.writerow({
                "id": rec.get("id", ""),
                "title": rec.get("title", ""),
                "insight": rec.get("insight", ""),
                "affected_entity": rec.get("affected_entity", ""),
                "priority": rec.get("priority", ""),
                "suggested_action": rec.get("suggested_action", ""),
            })
        dl_name = f"{filename_base}_recommendations.csv"

    else:
        # KPIs summary
        writer = csv.DictWriter(stream, fieldnames=["label", "value"])
        writer.writeheader()
        for kpi in dashboard.get("kpis", []):
            # Export the raw numeric value for better Excel compatibility, fallback to formatted value
            writer.writerow({"label": kpi.get("label", ""), "value": kpi.get("raw", kpi.get("value", ""))})
        dl_name = f"{filename_base}_kpis.csv"

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename={dl_name}"
    return response


# ── Delete workspace ────────────────────────────────────────────────────────

@router.delete("/datasets/{dataset_id}")
def delete_dataset(dataset_id: str):
    ws = workspace_registry.get(dataset_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found.")
    workspace_registry.delete(dataset_id)
    return {"dataset_id": dataset_id, "message": "Workspace deleted."}
