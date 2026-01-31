from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
  """기본 Repository (재사용 가능한 CRUD 템플릿)"""

  def __init__(self, model: Type[ModelType], db: AsyncSession):
    self.model = model
    self.db = db

  async def create(self, schema: CreateSchemaType) -> ModelType:
    """데이터 생성"""
    db_obj = self.model(**schema.model_dump())
    self.db.add(db_obj)
    await self.db.commit()
    await self.db.refresh(db_obj)
    return db_obj

  async def get_by_id(self, id: int) -> ModelType | None:
    """ID로 조회"""
    result = await self.db.execute(
      select(self.model).where(self.model.id == id)
    )
    return result.scalar_one_or_none()

  async def get_all(self, skip: int = 0, limit: int = 10) -> list[ModelType]:
    """전체 목록 조회 (페이지네이션)"""
    result = await self.db.execute(
      select(self.model).offset(skip).limit(limit)
    )
    return list(result.scalars().all())

  async def update(self, id: int, schema: UpdateSchemaType) -> ModelType:
    """데이터 수정"""
    await self.db.execute(
      update(self.model)
      .where(self.model.id == id)
      .values(**schema.model_dump(exclude_unset=True))
    )
    await self.db.commit()
    return await self.get_by_id(id)

  async def delete(self, id: int) -> bool:
    """데이터 삭제"""
    result = await self.db.execute(
      delete(self.model).where(self.model.id == id)
    )
    await self.db.commit()
    return result.rowcount > 0
