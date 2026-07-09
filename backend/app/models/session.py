from __future__ import annotations

from beanie import Link
from pydantic import Field

from .base import BaseDocument
from .enums import Difficulty, SessionStatus
from .user import User


class Session(BaseDocument):
    problem_title: str = Field(alias="problemTitle")
    difficulty: Difficulty

    host: Link[User]
    participant: Link[User] | None = None

    status: SessionStatus = SessionStatus.ACTIVE

    # Stream video call ID
    call_id: str = Field(default="", alias="callId")

    class Settings:
        name = "sessions"
