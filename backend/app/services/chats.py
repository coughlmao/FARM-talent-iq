from app.integrations.stream import (
    create_stream_token,
    upsert_stream_user,
)
from app.models import User


async def get_unified_stream_token(
    current_user: User,
) -> dict[str, str]:
    # 1. Sync user data to Stream (shared by Chat and Video)
    await upsert_stream_user(current_user)

    # 2. Generate ONE token for this user
    # This token is valid for both Chat and Video clients
    token = create_stream_token(current_user.clerk_id)

    return {
        "token": token,
        "userId": current_user.clerk_id,
        "userName": current_user.name,
        "userImage": current_user.profile_image,
    }
