from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class SuccessResponse(BaseModel, Generic[T]):
  """표준 성공 응답 포맷"""

  success: bool = True
  data: T
  message: str | None = None


class ErrorResponse(BaseModel):
  """표준 에러 응답 포맷"""

  success: bool = False
  error: str
  detail: str | None = None
