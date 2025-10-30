from fastapi import APIRouter

from app.api.v1 import admin, chat, profile

api_router = APIRouter()

api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
