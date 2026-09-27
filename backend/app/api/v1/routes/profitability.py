from fastapi import APIRouter
from backend.app.services.data_service import data_service
from backend.app.schemas.dashboard import CategorySales
from backend.app.data.validation import clean_for_json
from typing import List

router = APIRouter()

@router.get("/profitability/summary")
def get_profitability_summary():
    df = data_service.get_df()
    grouped = df.groupby('sub_category').agg({'sales': 'sum', 'profit': 'sum'}).reset_index()
    
    res = []
    for _, row in grouped.iterrows():
        sales = clean_for_json(row['sales'])
        profit = clean_for_json(row['profit'])
        margin = (profit / sales * 100) if sales else 0
        res.append({
            "name": clean_for_json(row['sub_category']),
            "sales": sales,
            "profit": profit,
            "margin": margin
        })
    
    sorted_res = sorted(res, key=lambda x: x['margin'], reverse=True)
    return {
        "top_performers": sorted_res[:5],
        "bottom_performers": sorted_res[-5:] if len(sorted_res) > 5 else sorted_res
    }
