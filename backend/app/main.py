from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import inngest.fast_api

from .lib.inngest import inngest_client, sync_user, delete_user
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

inngest.fast_api.serve(
    app,
    inngest_client,
    [sync_user, delete_user],
    
    serve_path="/api/inngest"
)

# API routes FIRST
app.include_router(chatRoutes, prefix="/api/chats")

# ---------- FRONTEND ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../frontend/dist"))

print("FRONTEND_BUILD_PATH =", FRONTEND_BUILD_PATH)
print("FILES =", os.listdir(FRONTEND_BUILD_PATH))

if settings.ENV_TYPE == "production":
    # root
    @app.get("/")
    async def root():
        return FileResponse(os.path.join(FRONTEND_BUILD_PATH, "index.html"))

    # catch-all for SPA routing + assets
    @app.get("/{path:path}")
    async def spa(path: str):
        file_path = os.path.join(FRONTEND_BUILD_PATH, path)

        # serve the file if it exists
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return FileResponse(file_path)

        # otherwise fallback to index.html
        return FileResponse(os.path.join(FRONTEND_BUILD_PATH, "index.html"))
