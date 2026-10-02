from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict

class PredictionRequest(BaseModel):
    category: str
    sub_category: str
    segment: str
    region: str
    market: str
    ship_mode: str
    sales: float = Field(gt=0)
    quantity: int = Field(gt=0)
    discount: float = Field(ge=0, le=1)
    shipping_cost: float = Field(ge=0)

class PredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    predicted_profit: float
    model_name: str
    model_version: str
    caveat: str

class ModelStatus(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    available: bool
    model_name: Optional[str] = None
    metrics: Optional[Dict] = None
    features: Optional[List[str]] = None
    created_at: Optional[str] = None
