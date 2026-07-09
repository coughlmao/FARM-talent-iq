from typing import Annotated  # for modern Python type hinting

from beanie import Indexed
from pydantic import EmailStr

from .base import BaseDocument


class User(BaseDocument):
    # Use Annotated with Indexed for the most reliable index creation
    clerk_id: Annotated[str, Indexed(unique=True)]
    email: EmailStr
    name: str
    profile_image: str = ""

    class Settings:
        name = "users"  # MongoDB collection name
