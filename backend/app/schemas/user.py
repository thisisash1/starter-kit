from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
  """공통 필드"""

  name: str
  email: EmailStr
  age: int | None = None


class UserCreate(UserBase):
  """사용자 생성 DTO"""

  pass


class UserUpdate(BaseModel):
  """사용자 수정 DTO (모든 필드 선택적)"""

  name: str | None = None
  email: EmailStr | None = None
  age: int | None = None


class UserResponse(UserBase):
  """사용자 응답 DTO"""

  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)  # ORM 모델 변환 허용
