from fastapi import APIRouter
from backend.app.services.data_service import data_service
from backend.app.schemas.analytics import SegmentAnalytics
from backend.app.data.validation import clean_for_json
from typing import List

router = APIRouter()

@router.get("/customers/segments", response_model=List[SegmentAnalytics])
def get_customer_segments():
    df = data_service.get_df()
    grouped = df.groupby('segment').agg({
        'sales': 'sum',
        'profit': 'sum',
        'order_id': 'nunique',
        'customer_name': 'nunique'
    }).reset_index()
    
    res = []
    for _, row in grouped.iterrows():
        sales = clean_for_json(row['sales'])
        profit = clean_for_json(row['profit'])
        orders = clean_for_json(row['order_id'])
        margin = (profit / sales * 100) if sales else 0
        avg_order = (sales / orders) if orders else 0
        
        res.append(SegmentAnalytics(
            segment=clean_for_json(row['segment']),
            sales=sales,
            profit=profit,
            orders=orders,
            customers=clean_for_json(row['customer_name']),
            avg_order_value=avg_order,
            margin=margin
        ))
    return res
