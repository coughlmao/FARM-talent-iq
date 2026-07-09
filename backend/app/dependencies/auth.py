from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.core.logger import logger
from app.integrations.clerk import get_clerk_signing_key
from app.models import User
from app.repositories.user import get_by_clerk_id

security = HTTPBearer()

AuthCredentials = Annotated[
    HTTPAuthorizationCredentials,
    Depends(security),
]


async def get_current_user(
    auth: AuthCredentials,
) -> User:
    token = auth.credentials

    try:
        signing_key = await get_clerk_signing_key(token)

        payload = jwt.decode(
            token,
            key=signing_key,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
                "leeway": 60,
            },
        )

        clerk_id = payload.get("sub")

        if clerk_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token.",
            )

        user = await get_by_clerk_id(clerk_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

        return user

    except HTTPException:
        raise

    except JWTError as exc:
        logger.warning(
            "Invalid Clerk JWT.",
            exc_info=exc,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token.",
        ) from exc

    except Exception as exc:
        logger.exception(
            "Authentication failed.",
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed.",
        ) from exc


CurrentUser = Annotated[
    User,
    Depends(get_current_user),
]
