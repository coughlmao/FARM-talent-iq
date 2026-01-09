from fastapi import FastAPI
from contextlib import asynccontextmanager

from .core.db import connectDB, closeDB
from .api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connectDB()
    print("[lifespan] Server running on FastAPI 🚀")
    print("🏠 Home: http://127.0.0.1:8000")
    print("📝 Swagger: http://127.0.0.1:8000/docs")
    yield
    await closeDB()

app = FastAPI(lifespan=lifespan)

app.include_router(router)