from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import inngest.fast_api
import asyncio

from .lib.inngest import inngest_client, sync_user, delete_user
from .lib.db import connect_db, close_db
from .routes.chats import router as chatRoutes
from .lib.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DEBUG: Starting application lifespan...")
    try:
        # Wrap the DB connection in a timeout (e.g., 10 seconds)
        # This prevents the "Waiting for application startup" hang
        await asyncio.wait_for(connect_db(), timeout=10.0)
        print("DEBUG: Database connected successfully!")
    except asyncio.TimeoutError:
        print("ERROR: Database connection timed out during startup!")
        # Raising an error here allows Render to see the crash instead of hanging 502
        raise RuntimeError("Database connection timeout")
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

# ---------- FRONTEND ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../frontend/dist"))

print("FRONTEND_BUILD_PATH =", FRONTEND_BUILD_PATH)
print("FILES =", os.listdir(FRONTEND_BUILD_PATH))

if settings.ENV_TYPE == "production":
    # root
    @app.api_route("/", methods=["GET", "HEAD"])
    async def root():
        return FileResponse(os.path.join(FRONTEND_BUILD_PATH, "index.html"))

    # catch-all for SPA routing + assets
    @app.api_route("/{path:path}", methods=["GET", "HEAD"])
    async def spa(path: str):
        file_path = os.path.join(FRONTEND_BUILD_PATH, path)

        # serve the file if it exists
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            return FileResponse(file_path)

        # otherwise fallback to index.html
        return FileResponse(os.path.join(FRONTEND_BUILD_PATH, "index.html"))
