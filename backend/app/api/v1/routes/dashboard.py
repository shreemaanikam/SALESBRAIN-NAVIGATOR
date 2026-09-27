from fastapi import APIRouter, Query
from typing import Optional
from backend.app.services.data_service import data_service
from backend.app.schemas.dashboard import DashboardKPIs, KPIMetric, DashboardTrends, TrendPoint
from backend.app.data.validation import clean_for_json
import pandas as pd

router = APIRouter()

@router.get("/dashboard/kpis", response_model=DashboardKPIs)
def get_dashboard_kpis():
    df = data_service.get_df()
    
    total_sales = float(df['sales'].sum())
    total_profit = float(df['profit'].sum())
    profit_margin = float((total_profit / total_sales) * 100) if total_sales > 0 else 0.0
    unique_orders = int(df['order_id'].nunique())
    avg_order_value = float(total_sales / unique_orders) if unique_orders > 0 else 0.0
    total_quantity = int(df['quantity'].sum())
    avg_discount = float(df['discount'].mean())
    leading_category = str(df.groupby('category')['sales'].sum().idxmax())
    
    metrics = [
        KPIMetric(label="Total Sales", value=f"${total_sales:,.2f}", trend="neutral"),
        KPIMetric(label="Total Profit", value=f"${total_profit:,.2f}", trend="neutral"),
        KPIMetric(label="Profit Margin", value=f"{profit_margin:.2f}%", trend="neutral"),
        KPIMetric(label="Unique Orders", value=str(unique_orders), trend="neutral"),
        KPIMetric(label="Avg Order Value", value=f"${avg_order_value:,.2f}", trend="neutral"),
        KPIMetric(label="Total Quantity", value=str(total_quantity), trend="neutral"),
        KPIMetric(label="Avg Discount", value=f"{avg_discount:.2%}", trend="neutral"),
        KPIMetric(label="Leading Category", value=leading_category, trend="neutral")
    ]
    return DashboardKPIs(metrics=metrics)

@router.get("/dashboard/trends", response_model=DashboardTrends)
def get_dashboard_trends(year: Optional[int] = Query(None)):
    df = data_service.get_df()
    if year:
        df = df[df['year'] == year]
        
    trend_df = df.groupby(['year', 'Month']).agg({
        'sales': 'sum',
        'profit': 'sum',
        'Month_Name': 'first'
    }).reset_index().sort_values(['year', 'Month'])
    
    data = []
    for _, row in trend_df.iterrows():
        period = f"{clean_for_json(row['Month_Name'])} {clean_for_json(row['year'])}"
        data.append(TrendPoint(
            period=period,
            sales=clean_for_json(row['sales']),
            profit=clean_for_json(row['profit'])
        ))
        
    return DashboardTrends(data=data, granularity="month")
