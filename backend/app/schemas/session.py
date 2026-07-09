from datetime import datetime

from pydantic import Field

from app.models.enums import Difficulty, SessionStatus

from .base import BaseSchema


class SessionCreateRequest(BaseSchema):
    problem_title: str = Field(
        alias="problemTitle",
        min_length=1,
        description="Title of the coding problem.",
    )

    difficulty: Difficulty = Field(description="Difficulty level.")


class UserSummary(BaseSchema):
    id: str
    name: str
    profile_image: str | None


class SessionRead(BaseSchema):
    id: str
    problem_title: str
    difficulty: Difficulty
    status: SessionStatus
    call_id: str
    host: UserSummary
    participant: UserSummary | None
    created_at: datetime
    updated_at: datetime


class SessionListResponse(BaseSchema):
    sessions: list[SessionRead]


class SessionDetailResponse(BaseSchema):
    session: SessionRead


class SessionCreateResponse(BaseSchema):
    session: SessionRead
    stream_token: str
    stream_api_key: str
    user_id: str


class SessionJoinResponse(BaseSchema):
    session: SessionRead


class SessionEndResponse(BaseSchema):
    session: SessionRead
    message: str
