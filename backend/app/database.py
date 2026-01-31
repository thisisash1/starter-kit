from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import settings

# Async 엔진 생성
engine = create_async_engine(
  settings.DATABASE_URL,
  echo=settings.DEBUG,  # SQL 로깅 (개발 환경에서만)
  pool_pre_ping=True,   # 연결 상태 확인
  pool_size=10,         # 연결 풀 크기
  max_overflow=20       # 최대 추가 연결
)

# 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
  engine,
  class_=AsyncSession,
  expire_on_commit=False,
  autocommit=False,
  autoflush=False
)


async def get_db() -> AsyncSession:
  """데이터베이스 세션 의존성"""
  async with AsyncSessionLocal() as session:
    try:
      yield session
    finally:
      await session.close()
