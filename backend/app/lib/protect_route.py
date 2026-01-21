from typing import Annotated

from clerk_backend_api import Clerk
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from ..models import User
from .clerk import get_clerk_Jwks
from .config import settings

clerk_client = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
security = HTTPBearer()

AuthDep = Annotated[HTTPAuthorizationCredentials, Depends(security)]


async def protect_route(auth: AuthDep):
    token = auth.credentials

    try:
        signing_key = await get_clerk_Jwks(token)

        payload = jwt.decode(
            token,
            key=signing_key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
                "leeway": 60,  # Allows 60s difference between frontend and backend clocks
            },
        )

        clerk_id = payload.get("sub")
        if not clerk_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject",
            )

        user = await User.find_one({"clerk_id": clerk_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    except JWTError as err:
        print(f"JWT Verification Error: {err}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        ) from err
    except Exception as err:
        print(f"Error in protect_route dependency: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from err
