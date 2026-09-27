from pydantic import BaseModel
from typing import Dict

class RecommendationItem(BaseModel):
    id: str
    title: str
    insight: str
    affected_entity: str
    metric_values: Dict
    suggested_action: str
    priority: str
    source: str
    limitations: str
