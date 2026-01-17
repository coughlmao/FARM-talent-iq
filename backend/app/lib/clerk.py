import httpx
from fastapi import Header, HTTPException
from jose import JWTError, jwt

from app.lib.config import settings

_jwksCache = None


async def get_clerk_Jwks():
    """
    Fetch JWKS from Clerk Frontend API with caching.
    Uses async httpx instead of requests for non-blocking calls.
    """
    global _jwksCache
    if _jwksCache is None:
        url = f"{settings.CLERK_FRONTEND_API}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
            res.raise_for_status()  # raise exception for non-200 status
            _jwksCache = res.json()
    return _jwksCache


async def verify_clerk_token(authorization: str = Header(...)):
    """
    FastAPI dependency to verify Clerk JWT token from Authorization header.
    Returns the decoded payload if valid.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]

    try:
        jwks = await get_clerk_Jwks()
        payload = jwt.decode(
            token, key=jwks, algorithms=["RS256"], options={"verify_aud": False}
        )
        return payload
    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err
