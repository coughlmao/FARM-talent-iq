from pymongo import AsyncMongoClient
from beanie import init_beanie

from .config import settings
from app.models import User

class MongoDB:
    client: AsyncMongoClient = None

conn = MongoDB()

async def connect_db():
    conn.client = AsyncMongoClient(settings.MONGO_URI)

    await init_beanie(
        database = conn.client[settings.MONGO_DB_NAME],
        document_models = [User],
    )

    print("[connectDB] Connected to MongoDB successfully")
    print(conn.client._host)

async def close_db():
    if conn.client:
        await conn.client.close()
        print("[closeDB] MongoDB connection closed")