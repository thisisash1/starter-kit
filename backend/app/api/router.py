from fastapi import APIRouter
from app.api.v1 import users

api_router = APIRouter()

# v1 API 라우트 등록
api_router.include_router(users.router, prefix="/v1")
