from fastapi import APIRouter

from app.api.routes.chats import router as chat_router
from app.api.routes.sessions import router as session_router

api_router = APIRouter()

api_router.include_router(session_router)
api_router.include_router(chat_router)
