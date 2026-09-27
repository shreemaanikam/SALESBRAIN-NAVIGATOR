from pydantic import BaseModel
from typing import List, Optional

class KPIMetric(BaseModel):
    label: str
    value: str
    trend: str
    trend_value: Optional[str] = None
    description: Optional[str] = None

class DashboardKPIs(BaseModel):
    metrics: List[KPIMetric]

class TrendPoint(BaseModel):
    period: str
    sales: float
    profit: float

class DashboardTrends(BaseModel):
    data: List[TrendPoint]
    granularity: str

class CategorySales(BaseModel):
    name: str
    sales: float
    profit: float
    margin: float
