from typing import Any

import httpx
from jose import jwt

from app.core.config import settings

_jwks_cache: dict[str, Any] | None = None


async def get_clerk_signing_key(
    token: str,
) -> dict[str, Any]:
    """
    Fetch JWKS from Clerk Frontend API with caching.
    Uses async httpx instead of requests for non-blocking calls.
    """
    global _jwks_cache
    if _jwks_cache is None:
        url = f"{settings.CLERK_FRONTEND_API}/.well-known/jwks.json"
        async with httpx.AsyncClient() as client:
            res = await client.get(url, timeout=10)
            res.raise_for_status()  # raise exception for non-200 status
            _jwks_cache = res.json()

    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    for key in _jwks_cache.get("keys", []):
        if key.get("kid") == kid:
            return key

    raise ValueError("Public key not found in JWKS")
