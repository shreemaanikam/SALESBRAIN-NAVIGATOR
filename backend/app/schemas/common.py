from pydantic import BaseModel, Field
from typing import Any, Optional, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Success"
    timestamp: str

class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)

class FilterParams(BaseModel):
    category: Optional[str] = None
    region: Optional[str] = None
    market: Optional[str] = None
    segment: Optional[str] = None
    sub_category: Optional[str] = None

class DateFilter(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
