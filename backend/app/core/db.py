from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.core.logger import logger
from app.models import Session, User


class MongoDB:
    client: AsyncMongoClient | None = None


db = MongoDB()


async def connect_db() -> None:
    db.client = AsyncMongoClient(
        settings.MONGO_URI,
        maxPoolSize=10,
        minPoolSize=1,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
    )

    # Explicitly connect and trigger DNS resolution before proceeding
    await db.client.aconnect()

    await init_beanie(
        database=db.client[settings.MONGO_DB_NAME],
        document_models=[
            User,
            Session,
        ],
    )

    logger.info("Connected to MongoDB successfully")


async def close_db() -> None:
    if db.client:
        db.client.close()
        logger.info("MongoDB connection closed")
