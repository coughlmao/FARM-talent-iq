from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import close_db, connect_db
from .logger import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("Connecting to MongoDB...")
    try:
        await asyncio.wait_for(connect_db(), timeout=60.0)
        logger.info("Database connected successfully.")
        yield

    except TimeoutError as err:
        logger.exception("Database connection timed out.")
        raise RuntimeError("Database connection timeout.") from err

    except Exception:
        logger.exception("Application startup failed.")

    finally:
        logger.info("Closing MongoDB connection...")
        await close_db()
