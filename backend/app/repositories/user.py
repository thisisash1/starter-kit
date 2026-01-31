from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
  """사용자 Repository"""

  def __init__(self, db: AsyncSession):
    super().__init__(User, db)

  async def get_by_email(self, email: str) -> User | None:
    """이메일로 사용자 조회"""
    result = await self.db.execute(
      select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()

  async def get_all(
    self,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
  ) -> list[User]:
    """사용자 목록 조회 (검색 기능 포함)"""
    query = select(User)

    # 검색 조건 추가
    if search:
      search_filter = or_(
        User.name.ilike(f"%{search}%"),
        User.email.ilike(f"%{search}%")
      )
      query = query.where(search_filter)

    query = query.offset(skip).limit(limit)
    result = await self.db.execute(query)
    return list(result.scalars().all())

  async def count(self, search: str | None = None) -> int:
    """전체 사용자 수 조회 (검색 포함)"""
    query = select(User)

    if search:
      search_filter = or_(
        User.name.ilike(f"%{search}%"),
        User.email.ilike(f"%{search}%")
      )
      query = query.where(search_filter)

    result = await self.db.execute(query)
    return len(result.scalars().all())
