from pydantic import BaseModel
from typing import Optional, Dict

class InsightItem(BaseModel):
    id: str
    type: str
    title: str
    description: str
    recommendation: Optional[str] = None
    impact: Optional[str] = None
    affected_entity: Optional[str] = None
    evidence: Optional[Dict] = None
    source: str
