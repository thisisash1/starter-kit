from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
  """페이지네이션 파라미터"""

  page: int = Field(default=1, ge=1, description="페이지 번호")
  page_size: int = Field(default=10, ge=1, le=100, description="페이지 크기")

  @property
  def skip(self) -> int:
    """건너뛸 레코드 수 계산"""
    return (self.page - 1) * self.page_size

  @property
  def limit(self) -> int:
    """조회할 레코드 수"""
    return self.page_size
