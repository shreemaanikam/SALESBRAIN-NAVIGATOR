from fastapi import APIRouter, Depends
from backend.app.services.data_service import data_service
from backend.app.schemas.common import FilterParams
from backend.app.data.validation import clean_for_json
from backend.app.schemas.analytics import RegionSales, MarketSales, MonthlySales

router = APIRouter()

def apply_filters(df, filters: FilterParams):
    if filters.category:
        df = df[df['category'] == filters.category]
    if filters.region:
        df = df[df['region'] == filters.region]
    if filters.market:
        df = df[df['market'] == filters.market]
    if filters.segment:
        df = df[df['segment'] == filters.segment]
    if filters.sub_category:
        df = df[df['sub_category'] == filters.sub_category]
    return df

@router.get("/sales/summary")
def get_sales_summary(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    total_sales = clean_for_json(df['sales'].sum())
    total_profit = clean_for_json(df['profit'].sum())
    return {"sales": total_sales, "profit": total_profit}

@router.get("/sales/by-category")
def get_sales_by_category(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby('category').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
    return grouped.to_dict('records')

@router.get("/sales/by-region")
def get_sales_by_region(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby('region').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).reset_index()
    return [RegionSales(
        region=clean_for_json(row['region']),
        sales=clean_for_json(row['sales']),
        profit=clean_for_json(row['profit']),
        orders=clean_for_json(row['order_id']),
        margin=clean_for_json((row['profit']/row['sales']*100) if row['sales'] else 0)
    ) for _, row in grouped.iterrows()]

@router.get("/sales/by-market")
def get_sales_by_market(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby('market').agg({'sales': 'sum', 'profit': 'sum', 'order_id': 'nunique'}).reset_index()
    return [MarketSales(
        market=clean_for_json(row['market']),
        sales=clean_for_json(row['sales']),
        profit=clean_for_json(row['profit']),
        orders=clean_for_json(row['order_id']),
        margin=clean_for_json((row['profit']/row['sales']*100) if row['sales'] else 0)
    ) for _, row in grouped.iterrows()]

@router.get("/sales/monthly")
def get_sales_monthly(filters: FilterParams = Depends()):
    df = apply_filters(data_service.get_df(), filters)
    grouped = df.groupby(['year', 'Month', 'Month_Name']).agg({'sales': 'sum', 'profit': 'sum'}).reset_index().sort_values(['year', 'Month'])
    return [MonthlySales(
        year=clean_for_json(row['year']),
        month=clean_for_json(row['Month']),
        month_name=clean_for_json(row['Month_Name']),
        sales=clean_for_json(row['sales']),
        profit=clean_for_json(row['profit'])
    ) for _, row in grouped.iterrows()]
