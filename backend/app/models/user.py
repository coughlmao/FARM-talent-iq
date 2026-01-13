from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone


class User(Document):
    clerk_id: str = Field(..., unique=True)
    email: EmailStr
    name: str
    profile_image: str = ""

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "users"  # MongoDB collection name