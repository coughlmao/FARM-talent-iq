from datetime import datetime
from typing import Any, Optional

from bson import ObjectId
from pydantic import ConfigDict, Field, field_validator

from app.models.enums import Difficulty

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
    profile_image: str | None = Field(default=None, alias="profileImage")

    @field_validator("id", mode="before")
    @classmethod
    def transform_id(cls, v: Any) -> str:
        # Handles raw ObjectIds or Beanie document models cleanly
        if isinstance(v, ObjectId):
            return str(v)
        if hasattr(v, "id"):
            return str(v.id)
        return str(v)


class SessionRead(BaseSchema):
    model_config = ConfigDict(populate_by_name=True)

    # Replicate Mongoose identity footprint exactly
    id: str = Field(alias="id")
    id_alias: str = Field(alias="_id")

    problemTitle: str = Field(alias="problemTitle")  # noqa: N815
    difficulty: str
    status: str
    callId: str = Field(alias="callId")  # noqa: N815
    host: Any
    participant: Optional[Any] = None  # noqa: UP045
    createdAt: datetime = Field(alias="createdAt")  # noqa: N815
    updatedAt: datetime = Field(alias="updatedAt")  # noqa: N815


class SessionListResponse(BaseSchema):
    sessions: list[SessionRead]


class SessionDetailResponse(BaseSchema):
    session: SessionRead


class SessionCreateResponse(BaseSchema):
    model_config = ConfigDict(populate_by_name=True)

    session: SessionRead
    streamToken: str = Field(alias="streamToken")  # noqa: N815
    streamApiKey: str = Field(alias="streamApiKey")  # noqa: N815
    userId: str = Field(alias="userId")  # noqa: N815


class SessionJoinResponse(BaseSchema):
    session: SessionRead


class SessionEndResponse(BaseSchema):
    session: SessionRead
    message: str
