from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class RegionSales(BaseModel):
    region: str
    sales: float
    profit: float
    orders: int
    margin: float

class MarketSales(BaseModel):
    market: str
    sales: float
    profit: float
    orders: int
    margin: float

class SegmentAnalytics(BaseModel):
    segment: str
    sales: float
    profit: float
    orders: int
    customers: int
    avg_order_value: float
    margin: float

class CountryAnalytics(BaseModel):
    country: str
    market: str
    region: str
    sales: float
    profit: float
    orders: int
    margin: float

class MonthlySales(BaseModel):
    year: int
    month: int
    month_name: str
    sales: float
    profit: float

class OutlierRecord(BaseModel):
    id: str
    order_id: str
    sales: float
    profit: float
    margin: float
    discount: float
    type: str
    severity: str

class OutlierSummary(BaseModel):
    lower_fence: float
    upper_fence: float
    total_outliers: int
    outlier_pct: float
    records: List[OutlierRecord]

class ColumnInfo(BaseModel):
    name: str
    dtype: str
    description: str
    non_null_count: int
    sample_values: List[Any]

class DataQuality(BaseModel):
    row_count: int
    column_count: int
    missing_values: Dict[str, int]
    date_range: Dict[str, Optional[str]]
    duplicates: int
    columns: List[ColumnInfo]
