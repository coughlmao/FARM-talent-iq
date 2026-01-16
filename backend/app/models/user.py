from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Annotated  # for modern Python type hinting


class User(Document):
    # Use Annotated with Indexed for the most reliable index creation
    clerk_id: Annotated[str, Indexed(unique=True)]
    email: EmailStr
    name: str
    profile_image: str = ""

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"  # MongoDB collection name
        validate_on_save=True
