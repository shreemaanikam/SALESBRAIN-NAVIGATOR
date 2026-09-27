import os
base_dir = "/Users/shreemaanikam/SalesBrainNavigator"

insights_route = """from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from backend.app.schemas.insight import InsightItem
from backend.app.schemas.recommendation import RecommendationItem
from backend.app.services.recommendation_service import recommendation_service
from backend.app.services.risk_service import risk_service
from backend.app.services.data_service import data_service

router = APIRouter()

@router.get("/insights", response_model=List[InsightItem])
def get_insights(
    category: Optional[str] = None,
    region: Optional[str] = None,
    market: Optional[str] = None
):
    df = data_service.get_df()
    recs = recommendation_service.generate_recommendations(df, category, region, market)
    risks = risk_service.get_risks(df, category, region, limit=10)
    
    insights = []
    for r in recs:
        insights.append(InsightItem(
            id=r['id'],
            type="recommendation",
            title=r['title'],
            description=r['insight'],
            recommendation=r['suggested_action'],
            affected_entity=r['affected_entity'],
            evidence=r['metric_values'],
            source=r['source']
        ))
        
    for r in risks:
        insights.append(InsightItem(
            id=r['id'],
            type=r['type'],
            title=f"Risk: {r['type']}",
            description=r['recommended_action'],
            impact=r['severity'],
            affected_entity=r['affected_entity'],
            evidence=r['evidence'],
            source=r['detection_method']
        ))
        
    return insights

@router.get("/recommendations", response_model=List[RecommendationItem])
def get_recommendations(
    category: Optional[str] = None,
    region: Optional[str] = None,
    market: Optional[str] = None
):
    df = data_service.get_df()
    recs = recommendation_service.generate_recommendations(df, category, region, market)
    return [RecommendationItem(**r) for r in recs]

@router.get("/recommendations/{recommendation_id}")
def get_recommendation(recommendation_id: str):
    df = data_service.get_df()
    recs = recommendation_service.generate_recommendations(df)
    for r in recs:
        if r['id'] == recommendation_id:
            return RecommendationItem(**r)
    raise HTTPException(status_code=404, detail="Recommendation not found")
"""

explanations_route = """from fastapi import APIRouter
from backend.app.schemas.prediction import PredictionRequest
from backend.app.services.explanation_service import explanation_service

router = APIRouter()

@router.get("/explanations/global")
def get_global_explanation():
    return explanation_service.global_explanation()

@router.post("/explanations/prediction")
def get_local_explanation(request: PredictionRequest):
    return explanation_service.local_explanation(request.model_dump())
"""

reports_route = """from fastapi import APIRouter, HTTPException
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
"""

router_update = """from fastapi import APIRouter
from backend.app.api.v1.routes import health, dashboard, sales, products, customers, geography, profitability, outliers, data_routes
from backend.app.api.v1.routes import predictions, insights, explanations, scenarios, reports

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(dashboard.router, tags=["dashboard"])
api_router.include_router(sales.router, tags=["sales"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(customers.router, tags=["customers"])
api_router.include_router(geography.router, tags=["geography"])
api_router.include_router(profitability.router, tags=["profitability"])
api_router.include_router(outliers.router, tags=["outliers"])
api_router.include_router(data_routes.router, tags=["data"])

# New routes
api_router.include_router(predictions.router, tags=["predictions"])
api_router.include_router(insights.router, tags=["insights"])
api_router.include_router(explanations.router, tags=["explanations"])
api_router.include_router(scenarios.router, tags=["scenarios"])
api_router.include_router(reports.router, tags=["reports"])
"""

with open(os.path.join(base_dir, "backend/app/api/v1/routes/insights.py"), "w") as f: f.write(insights_route)
with open(os.path.join(base_dir, "backend/app/api/v1/routes/explanations.py"), "w") as f: f.write(explanations_route)
with open(os.path.join(base_dir, "backend/app/api/v1/routes/reports.py"), "w") as f: f.write(reports_route)
with open(os.path.join(base_dir, "backend/app/api/v1/router.py"), "w") as f: f.write(router_update)

