from fastapi import FastAPI
from app.core.db import connectDB
from app.api.routes import router


app = FastAPI()

@app.on_event("startServer")
async def startServer():
    await connectDB()

app.include_router(router)