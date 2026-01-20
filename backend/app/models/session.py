from datetime import UTC, datetime
from enum import Enum

from beanie import Document, Link
from pydantic import Field

from .user import User


# Defining Enums
class Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class SessionStatus(str, Enum):
    active = "active"
    completed = "completed"


class Session(Document):
    problem_title: str = Field(alias="problemTitle")
    difficulty: Difficulty

    # References(Equivalent to ref:"User")
    # Link handles MongoDB ObjectIDs and DB preferences automatically

    host: Link["User"]
    participant: Link["User"] | None = None

    status: SessionStatus = SessionStatus.active

    # Stream video call ID
    call_id: str = Field(default="", alias="callId")

    # TimeStamps(Equivalent to {timestamps:true})
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        name = "sessions"
        validate_on_save = True
