from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


def configure_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.CLIENT_URL],
        allow_credentials=True,  # Crucial for session/auth endpoints
        allow_methods=["*"],  # Permits all necessary HTTP verbs
        allow_headers=["*"],  # Prevents unexpected header rejections
    )
