from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .lib.db import connect_db, close_db
from .routes.chats import router as chatRoutes
from .lib.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes FIRST
app.include_router(chatRoutes, prefix="/api/chats")


# ---------- FRONTEND ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "../../../frontend/dist")
)

print("FRONTEND_BUILD_PATH =", FRONTEND_BUILD_PATH)
print("FILES =", os.listdir(FRONTEND_BUILD_PATH))

if settings.ENV_TYPE == "production":
    app.mount(
        "/assets",
        StaticFiles(directory=os.path.join(FRONTEND_BUILD_PATH, "assets")),
        name="assets",
    )

    @app.get("/{path:path}")
    async def serve_react(path: str):
        file_path = os.path.join(FRONTEND_BUILD_PATH, path)

        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return FileResponse(file_path)

        return FileResponse(os.path.join(FRONTEND_BUILD_PATH, "index.html"))
