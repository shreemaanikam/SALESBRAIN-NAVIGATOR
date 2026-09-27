from pydantic import BaseModel, Field
from typing import Optional, List

class ScenarioBaseline(BaseModel):
    category: str
    sub_category: str
    segment: str
    region: str
    market: str
    ship_mode: str
    sales: float
    quantity: int
    discount: float
    shipping_cost: float

class ScenarioModifiers(BaseModel):
    discount_delta: float = 0.0
    quantity_change_pct: float = 0.0
    shipping_cost_change_pct: float = 0.0
    sales_change_pct: float = 0.0

class SimulationRequest(BaseModel):
    baseline: ScenarioBaseline
    scenario: ScenarioModifiers

class SimulationResponse(BaseModel):
    baseline_profit: float
    scenario_profit: float
    absolute_delta: float
    pct_delta: Optional[float]
    risk_level: str
    assumptions: List[str]
    warnings: List[str]
    model_version: str
    mode: str = 'model'
