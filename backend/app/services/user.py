from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.exceptions import NotFoundException, DuplicateException


class UserService:
  """사용자 서비스"""

  def __init__(self, db: AsyncSession):
    self.repository = UserRepository(db)

  async def create_user(self, user_data: UserCreate) -> UserResponse:
    """사용자 생성 비즈니스 로직"""
    # 이메일 중복 검사
    existing_user = await self.repository.get_by_email(user_data.email)
    if existing_user:
      raise DuplicateException("이미 존재하는 이메일입니다")

    # 사용자 생성
    user = await self.repository.create(user_data)
    return UserResponse.model_validate(user)

  async def get_users(
    self,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
  ) -> tuple[list[UserResponse], int]:
    """사용자 목록 조회 (검색 포함) 및 전체 개수 반환"""
    users = await self.repository.get_all(
      skip=skip,
      limit=limit,
      search=search
    )
    total_count = await self.repository.count(search=search)
    return [UserResponse.model_validate(user) for user in users], total_count

  async def get_user_by_id(self, user_id: int) -> UserResponse:
    """사용자 상세 조회"""
    user = await self.repository.get_by_id(user_id)
    if not user:
      raise NotFoundException(f"사용자를 찾을 수 없습니다 (ID: {user_id})")

    return UserResponse.model_validate(user)

  async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
    """사용자 정보 수정"""
    user = await self.repository.get_by_id(user_id)
    if not user:
      raise NotFoundException(f"사용자를 찾을 수 없습니다 (ID: {user_id})")

    # 이메일 변경 시 중복 검사
    if user_data.email and user_data.email != user.email:
      existing_user = await self.repository.get_by_email(user_data.email)
      if existing_user:
        raise DuplicateException("이미 존재하는 이메일입니다")

    updated_user = await self.repository.update(user_id, user_data)
    return UserResponse.model_validate(updated_user)

  async def delete_user(self, user_id: int) -> bool:
    """사용자 삭제"""
    user = await self.repository.get_by_id(user_id)
    if not user:
      raise NotFoundException(f"사용자를 찾을 수 없습니다 (ID: {user_id})")

    return await self.repository.delete(user_id)
