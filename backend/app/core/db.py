from pymongo import AsyncMongoClient

from .config import settings

class MongoDB:
    client: AsyncMongoClient = None

conn = MongoDB()

async def connectDB():
    conn.client = AsyncMongoClient(settings.MONGO_URI)
    print("[connectDB] Connected to MongoDB successfully")

async def closeDB():
    if conn.client:
        await conn.client.close()
        print("[closeDB] MongoDB connection closed")