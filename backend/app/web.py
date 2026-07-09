from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, Response

from app.core.config import settings

APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent.parent

FRONTEND_DIR = PROJECT_ROOT / "frontend" / "dist"
INDEX_FILE = FRONTEND_DIR / "index.html"


def register_frontend(app: FastAPI) -> None:
    """
    Register SPA Routes when running in production
    """

    if settings.ENV_TYPE != "production":
        return

    @app.get("/", include_in_schema=False)
    async def root() -> Response:
        if INDEX_FILE.exists():
            return FileResponse(INDEX_FILE)
        return {"error": "Frontend build not found."}

    @app.get("/{path:path}", include_in_schema=False)
    async def spa(path: str) -> Response:
        file = FRONTEND_DIR / path

        if file.exists() and file.is_file():
            return FileResponse(file)

        if INDEX_FILE.exists():
            return FileResponse(INDEX_FILE)
        return {"error": "Frontend build not found."}
