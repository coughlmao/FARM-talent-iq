from datetime import UTC, datetime

from beanie import Document
from pydantic import Field


class BaseDocument(Document):
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        validate_on_save = True
