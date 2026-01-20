import asyncio
import os
from contextlib import asynccontextmanager

import inngest.fast_api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .lib.config import settings
from .lib.db import close_db, connect_db
from .lib.inngest import delete_user, inngest_client, sync_user
from .routes.chats import router as chatRoutes
from .routes.sessions import router as sessionRoutes


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DEBUG: Starting application lifespan...")
    try:
        # Wrap the DB connection in a timeout (e.g., 10 seconds)
        # This prevents the "Waiting for application startup" hang
        await asyncio.wait_for(connect_db(), timeout=60.0)
        print("DEBUG: Database connected successfully!")
    except TimeoutError as err:
        print("ERROR: Database connection timed out during startup!")
        # Raising an error here allows Render to see the crash instead of hanging 502
        raise RuntimeError("Database connection timeout") from err
    except Exception as e:
        print(f"ERROR: Startup failed with exception: {e}")
        raise e
    yield
    await close_db()


app = FastAPI(lifespan=lifespan)

# CORS must be handled before routing
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inngest Serve - Registering functions at /api/inngest
# The SDK automatically handles the POST and GET handshakes
inngest.fast_api.serve(
    app, inngest_client, [sync_user, delete_user], serve_path="/api/inngest"
)

# API routes FIRST
app.include_router(chatRoutes, prefix="/api/chats")
app.include_router(sessionRoutes, prefix="/api/sessions")

# ---------- FRONTEND ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../frontend/dist"))

print("FRONTEND_BUILD_PATH =", FRONTEND_BUILD_PATH)
print("FILES =", os.listdir(FRONTEND_BUILD_PATH))

if settings.ENV_TYPE == "production":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    FRONTEND_BUILD_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../frontend/dist"))
    INDEX_PATH = os.path.join(FRONTEND_BUILD_PATH, "index.html")

    # Serve the React/Vite root
    @app.api_route("/", methods=["GET", "HEAD"])
    async def root():
        if os.path.exists(INDEX_PATH):
            return FileResponse(INDEX_PATH)
        return {"error": "Frontend build not found"}

    # Catch-all for SPA routing (React Router / Vue Router)
    @app.api_route("/{path:path}", methods=["GET", "HEAD"])
    async def spa(path: str):
        file_path = os.path.join(FRONTEND_BUILD_PATH, path)

        # 1. Serve actual files (js, css, images)
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return FileResponse(file_path)

        # 2. Fallback to index.html for all other paths
        if os.path.exists(INDEX_PATH):
            return FileResponse(INDEX_PATH)

        return {"error": "File not found and index.html missing"}
