from pydantic import BaseModel
from typing import Optional, Dict, List

class ReportType(BaseModel):
    id: str
    name: str
    description: str
    formats: List[str]

class ExportRequest(BaseModel):
    report_type: str
    format: str = 'csv'
    filters: Optional[Dict] = None
