from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.services.user import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.responses import SuccessResponse
from app.core.pagination import PaginationParams

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=SuccessResponse[UserResponse], status_code=status.HTTP_201_CREATED)
async def create_user(
  user_data: UserCreate,
  db: AsyncSession = Depends(get_db)
) -> SuccessResponse[UserResponse]:
  """사용자 생성"""
  service = UserService(db)
  user = await service.create_user(user_data)
  return SuccessResponse(data=user)


@router.get("", response_model=SuccessResponse[dict])
async def get_users(
  page: int = 1,
  page_size: int = 10,
  search: str | None = None,
  db: AsyncSession = Depends(get_db)
) -> SuccessResponse[dict]:
  """사용자 목록 조회 (페이지네이션, 검색)"""
  # 페이지네이션 파라미터 검증
  if page < 1:
    page = 1
  if page_size < 1 or page_size > 100:
    page_size = 10

  skip = (page - 1) * page_size

  service = UserService(db)
  users, total_count = await service.get_users(
    skip=skip,
    limit=page_size,
    search=search
  )

  # 전체 페이지 수 계산
  total_pages = (total_count + page_size - 1) // page_size

  return SuccessResponse(data={
    "items": users,
    "total": total_count,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
  })


@router.get("/{user_id}", response_model=SuccessResponse[UserResponse])
async def get_user(
  user_id: int,
  db: AsyncSession = Depends(get_db)
) -> SuccessResponse[UserResponse]:
  """사용자 상세 조회"""
  service = UserService(db)
  user = await service.get_user_by_id(user_id)
  return SuccessResponse(data=user)


@router.put("/{user_id}", response_model=SuccessResponse[UserResponse])
async def update_user(
  user_id: int,
  user_data: UserUpdate,
  db: AsyncSession = Depends(get_db)
) -> SuccessResponse[UserResponse]:
  """사용자 정보 수정"""
  service = UserService(db)
  user = await service.update_user(user_id, user_data)
  return SuccessResponse(data=user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
  user_id: int,
  db: AsyncSession = Depends(get_db)
) -> None:
  """사용자 삭제"""
  service = UserService(db)
  await service.delete_user(user_id)
