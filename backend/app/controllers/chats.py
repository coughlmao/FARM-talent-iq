from ..lib.stream import client, upsert_stream_user
from ..models import User


async def get_unified_stream_token(current_user: User):
    # 1. Sync user data to Stream (shared by Chat and Video)
    await upsert_stream_user(
        {
            "id": current_user.clerk_id,
            "name": current_user.name,
            "image": current_user.profile_image,
        }
    )

    # 2. Generate ONE token for this user
    # This token is valid for both Chat and Video clients
    token = client.create_token(current_user.clerk_id)

    return {
        "token": token,
        "userId": current_user.clerk_id,
        "userName": current_user.name,
        "userImage": current_user.profile_image,
    }
