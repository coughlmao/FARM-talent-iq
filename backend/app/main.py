from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .lib.db import connect_db, close_db
from .routes.chats import router as chatRoutes
from .lib.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print("[lifespan] Server running on FastAPI 🚀")
    print("🏠 Home: http://127.0.0.1:8000")
    print("📝 Swagger: http://127.0.0.1:8000/docs")
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

app.include_router(chatRoutes, prefix="/api/chats")

FRONTEND_BUILD_PATH = "../frontend/dist"

if settings.ENV_TYPE == "production":
    app.mount(
        "/",
        StaticFiles(directory=FRONTEND_BUILD_PATH, html=True),
        name="frontend",
    )

    @app.get("/{path:path}")
    async def serve_react(path: str):
        return FileResponse(f"{FRONTEND_BUILD_PATH}/index.html")