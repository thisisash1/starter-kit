from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.router import api_router
from app.core.exceptions import AppException

app = FastAPI(
  title=settings.APP_NAME,
  description="FastAPI 백엔드 스타터킷",
  version="1.0.0",
  docs_url="/docs",      # Swagger UI
  redoc_url="/redoc"     # ReDoc
)

# CORS 설정 (프론트엔드 연동 시)
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # 운영에서는 특정 도메인만 허용
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# 전역 예외 핸들러

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
  """커스텀 예외 처리"""
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "success": False,
      "error": exc.message,
      "detail": None
    }
  )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
  """Pydantic 검증 에러 처리"""
  return JSONResponse(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    content={
      "success": False,
      "error": "입력값 검증 실패",
      "detail": exc.errors()
    }
  )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
  """예상치 못한 예외 처리"""
  return JSONResponse(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={
      "success": False,
      "error": "서버 내부 오류가 발생했습니다",
      "detail": str(exc) if settings.DEBUG else None
    }
  )


# API 라우터 등록
app.include_router(api_router, prefix="/api")


# 헬스 체크 엔드포인트

@app.get("/health")
async def health_check():
  """헬스 체크 엔드포인트"""
  return {"status": "healthy"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=settings.DEBUG
  )
