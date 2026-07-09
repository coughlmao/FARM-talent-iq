from fastapi import FastAPI

from app.api.router import api_router
from app.core.lifespan import lifespan
from app.core.middleware import configure_middleware
from app.integrations.inngest import register_inngest
from app.web import register_frontend

app = FastAPI(
    title="FARM TalentIQ API",
    summary="Backend for collaborative technical interviews.",
    version="1.0.0",
    lifespan=lifespan,
)

# ----------------------- Middleware -----------------------
configure_middleware(app)

register_inngest(app)

# ------------------------- Routes -------------------------
app.include_router(api_router)

# ----------------------- Production -----------------------
register_frontend(app)
