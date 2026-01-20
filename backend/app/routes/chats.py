from typing import Annotated

from fastapi import APIRouter, Depends

from ..controllers.chats import get_unified_stream_token
from ..lib.protect_route import protect_route
from ..models import User

router = APIRouter()

AuthDep = Annotated[User, Depends(protect_route)]


@router.get("/token")
async def get_unified_stream_token_route(current_user: AuthDep):
    return get_unified_stream_token()
