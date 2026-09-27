from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from backend.app.schemas.report import ReportType, ExportRequest
from backend.app.services.data_service import data_service

router = APIRouter()

@router.get("/reports/types")
def get_report_types():
    return [
        ReportType(id="executive", name="Executive Summary", description="High-level metrics", formats=["csv"]),
        ReportType(id="sales", name="Sales Report", description="Detailed sales data", formats=["csv"]),
        ReportType(id="profitability", name="Profitability", description="Profit analysis", formats=["csv"]),
        ReportType(id="products", name="Product Performance", description="Product metrics", formats=["csv"]),
        ReportType(id="risk", name="Risk Report", description="Identified risks", formats=["csv"]),
        ReportType(id="eda", name="EDA Data", description="Exploratory data", formats=["csv"])
    ]

@router.post("/reports/export")
def export_report(request: ExportRequest):
    df = data_service.get_df()
    if df.empty:
        raise HTTPException(status_code=400, detail="Data not available")
        
    if request.report_type == 'sales':
        cols = [c for c in ['order_id', 'order_date', 'sales', 'quantity', 'category', 'region'] if c in df.columns]
        export_df = df[cols]
    elif request.report_type == 'profitability':
        cols = [c for c in ['order_id', 'profit', 'Profit_Margin', 'discount', 'category'] if c in df.columns]
        export_df = df[cols]
    else:
        export_df = df.head(1000)
        
    stream = io.StringIO()
    export_df.to_csv(stream, index=False)
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=report_{request.report_type}.csv"
    return response
