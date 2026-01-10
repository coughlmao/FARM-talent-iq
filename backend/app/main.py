from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .lib.db import connectDB, closeDB
from .routes.chats import router as chatRoutes
from .lib.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connectDB()
    print("[lifespan] Server running on FastAPI 🚀")
    print("🏠 Home: http://127.0.0.1:8000")
    print("📝 Swagger: http://127.0.0.1:8000/docs")
    yield
    await closeDB()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatRoutes, prefix="/api/chats")
