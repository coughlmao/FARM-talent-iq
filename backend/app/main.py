import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


# -----------------MERN Execution pipeline------------
# Lint Fix: Replaced Optional[str] with modern 'str | None' type union
class ExecutionRequest(BaseModel):
    language: str
    code: str
    input: str | None = ""


# Create the endpoint that hits your MERN execution client URL directly
@app.post("/api/v1/execute")
async def handle_execution(payload: ExecutionRequest):
    # Lint Fix: Converted variable name inside function to lowercase snake_case
    mern_client_url = (
        "https://mern-interview-platform-talent-iq.onrender.com/api/execute"
    )

    payload_dict = {
        "language": payload.language,
        "code": payload.code,
        "input": payload.input,
    }

    try:
        # Use httpx to make a direct backend-to-backend request to MERN
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(mern_client_url, json=payload_dict)

            if response.status_code != 200:
                return {
                    "success": False,
                    "output": "",
                    "error": f"MERN service returned error status: {response.status_code}",
                }

            # Return the exact JSON structure coming back from your MERN controller
            return response.json()

    except httpx.RequestError as exc:
        # Lint Fix: Added explicit string conversion flag '!s'
        # Lint Fix: Raised the exception 'from exc' to cleanly handle context tracking
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to the MERN execution server: {exc!s}",
        ) from exc


# ------------------------- Routes -------------------------
app.include_router(api_router)

# ----------------------- Production -----------------------
register_frontend(app)
