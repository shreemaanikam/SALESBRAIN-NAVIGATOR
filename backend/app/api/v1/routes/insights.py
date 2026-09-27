from fastapi import APIRouter, Query, HTTPException
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
