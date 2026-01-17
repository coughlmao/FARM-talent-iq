from beanie import init_beanie
from pymongo import AsyncMongoClient

from ..models import Session, User
from .config import settings


class MongoDB:
    client: AsyncMongoClient = None


conn = MongoDB()


async def connect_db():
    conn.client = AsyncMongoClient(
        settings.MONGO_URI,
        maxPoolSize=10,
        minPoolSize=1,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
    )

    # Explicitly connect and trigger DNS resolution before proceeding
    await conn.client.aconnect()

    await init_beanie(
        database=conn.client[settings.MONGO_DB_NAME], document_models=[User, Session]
    )

    print("[connectDB] Connected to MongoDB successfully")
    print(conn.client._host)


async def close_db():
    if conn.client:
        conn.client.close()
        print("[closeDB] MongoDB connection closed")
