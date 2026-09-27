from fastapi import APIRouter
from backend.app.services.data_service import data_service
from backend.app.schemas.analytics import OutlierSummary, OutlierRecord
from backend.app.data.validation import clean_for_json

router = APIRouter()

@router.get("/outliers", response_model=OutlierSummary)
def get_outliers():
    df = data_service.get_df()
    
    Q1 = df['sales'].quantile(0.25)
    Q3 = df['sales'].quantile(0.75)
    IQR = Q3 - Q1
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR
    
    outliers_df = df[(df['sales'] < lower_fence) | (df['sales'] > upper_fence)]
    
    records = []
    for idx, row in outliers_df.iterrows():
        sales = clean_for_json(row['sales'])
        profit = clean_for_json(row['profit'])
        margin = (profit / sales * 100) if sales else 0
        severity = "High" if sales > (Q3 + 3 * IQR) or sales < (Q1 - 3 * IQR) else "Medium"
        
        records.append(OutlierRecord(
            id=str(idx),
            order_id=clean_for_json(row['order_id']),
            sales=sales,
            profit=profit,
            margin=margin,
            discount=clean_for_json(row['discount']),
            type="Sales Outlier",
            severity=severity
        ))
        
    return OutlierSummary(
        lower_fence=clean_for_json(lower_fence),
        upper_fence=clean_for_json(upper_fence),
        total_outliers=len(records),
        outlier_pct=clean_for_json(len(records) / len(df) * 100) if len(df) else 0,
        records=records
    )
