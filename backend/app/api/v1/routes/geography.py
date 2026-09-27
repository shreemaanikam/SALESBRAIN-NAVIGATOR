from fastapi import APIRouter, Depends
from backend.app.services.data_service import data_service
from backend.app.schemas.common import FilterParams
from backend.app.schemas.analytics import MarketSales, CountryAnalytics
from backend.app.data.validation import clean_for_json
from backend.app.api.v1.routes.sales import apply_filters
from typing import List

router = APIRouter()

@router.get("/geography/summary", response_model=List[MarketSales])
def get_geography_summary(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby('market').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).reset_index()
    return [MarketSales(
        market=clean_for_json(row['market']),
        sales=clean_for_json(row['sales']),
        profit=clean_for_json(row['profit']),
        orders=clean_for_json(row['order_id']),
        margin=clean_for_json((row['profit']/row['sales']*100) if row['sales'] else 0)
    ) for _, row in grouped.iterrows()]

@router.get("/geography/countries", response_model=List[CountryAnalytics])
def get_geography_countries(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby(['country', 'market', 'region']).agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).reset_index()
    grouped = grouped.sort_values('sales', ascending=False)
    
    return [CountryAnalytics(
        country=clean_for_json(row['country']),
        market=clean_for_json(row['market']),
        region=clean_for_json(row['region']),
        sales=clean_for_json(row['sales']),
        profit=clean_for_json(row['profit']),
        orders=clean_for_json(row['order_id']),
        margin=clean_for_json((row['profit']/row['sales']*100) if row['sales'] else 0)
    ) for _, row in grouped.iterrows()]
