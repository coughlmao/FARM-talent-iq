from fastapi import APIRouter

from app.dependencies.auth import CurrentUser
from app.services.chats import (
    get_unified_stream_token as get_unified_stream_token_service,
)

router = APIRouter(
    prefix="/api/chats",
    tags=["Chats"],
)


@router.get("/token")
async def get_unified_stream_token(current_user: CurrentUser):
    return await get_unified_stream_token_service(current_user)
