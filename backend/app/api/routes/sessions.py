from beanie import PydanticObjectId
from fastapi import APIRouter, status

from app.dependencies.auth import CurrentUser
from app.schemas.session import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionDetailResponse,
    SessionEndResponse,
    SessionJoinResponse,
    SessionListResponse,
)
from app.services.sessions import (
    create_session as create_session_controller,
    end_session as end_session_controller,
    get_session as get_session_controller,
    join_session as join_session_controller,
    list_active_sessions as list_active_sessions_controller,
    list_recent_sessions as list_recent_sessions_controller,
)

router = APIRouter(
    prefix="/api/sessions",
    tags=["Sessions"],
)


@router.post(
    "/",
    response_model=SessionCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_session(
    data: SessionCreateRequest,
    current_user: CurrentUser,
) -> SessionCreateResponse:
    return await create_session_controller(data, current_user)


@router.get(
    "/active",
    response_model=SessionListResponse,
)
async def list_active_sessions() -> SessionListResponse:
    return await list_active_sessions_controller()


@router.get(
    "/my-recent",
    response_model=SessionListResponse,
)
async def list_recent_sessions(
    current_user: CurrentUser,
) -> SessionListResponse:
    return await list_recent_sessions_controller(current_user)


@router.get(
    "/{session_id}",
    response_model=SessionDetailResponse,
)
async def get_session(session_id: PydanticObjectId) -> SessionDetailResponse:
    return await get_session_controller(session_id)


@router.post(
    "/{session_id}/join",
    response_model=SessionJoinResponse,
)
async def join_session(
    session_id: PydanticObjectId, current_user: CurrentUser
) -> SessionJoinResponse:
    return await join_session_controller(session_id, current_user)


@router.post(
    "/{session_id}/end",
    response_model=SessionEndResponse,
)
async def end_session(
    session_id: PydanticObjectId, current_user: CurrentUser
) -> SessionEndResponse:
    return await end_session_controller(session_id, current_user)
