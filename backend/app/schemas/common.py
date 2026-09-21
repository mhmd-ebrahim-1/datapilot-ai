from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar('T')

class ErrorResponse(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None

class SuccessResponse(BaseModel, Generic[T]):
    data: T
    message: str = "Success"

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
