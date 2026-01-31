from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class BaseResponse(BaseModel, Generic[T]):
  """기본 응답 스키마"""

  success: bool = True
  data: T | None = None
  message: str | None = None
