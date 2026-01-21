from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..controllers.sessions import (
    create_session,
    end_session,
    get_active_sessions,
    get_my_recent_session,
    get_session_by_id,
    join_session,
)
from ..lib.protect_route import protect_route
from ..models import User

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session_route(
    data: dict, current_user: Annotated[User, Depends(protect_route)]
):
    return await create_session(data, current_user)


@router.get("/active")
async def get_active_sessions_route():
    return await get_active_sessions()


@router.get("/my-recent")
async def get_my_recent_sessions_route(
    current_user: Annotated[User, Depends(protect_route)],
):
    return await get_my_recent_session(current_user)


@router.get("/{id}")
async def get_session_by_id_route(id: str):
    return await get_session_by_id(id)


@router.post("/{id}/join")
async def join_session_route(
    id: str, current_user: Annotated[User, Depends(protect_route)]
):
    return await join_session(id, current_user)


@router.post("/{id}/end")
async def end_session_route(
    id: str, current_user: Annotated[User, Depends(protect_route)]
):
    return await end_session(id, current_user)
