from pydantic import BaseModel
from typing import List, Optional

class ProductSummary(BaseModel):
    product_id: str
    name: str
    category: str
    sub_category: str
    total_sales: float
    total_profit: float
    profit_margin: float
    total_quantity: int
    avg_discount: float
    total_shipping_cost: float
    order_count: int
    risk_status: str

class ProductDetail(ProductSummary):
    markets: List[str]
    regions: List[str]
    countries: List[str]
    monthly_trend: List[dict]

class ProductListResponse(BaseModel):
    products: List[ProductSummary]
    total: int
    page: int
    page_size: int
