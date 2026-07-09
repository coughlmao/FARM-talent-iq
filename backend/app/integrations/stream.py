from getstream import Stream
from getstream.models import UserRequest

from app.core.config import settings
from app.core.logger import logger
from app.models import User

# Unified client for both chat and video
stream_client = Stream(
    api_key=settings.STREAM_API_KEY,
    api_secret=settings.STREAM_API_SECRET,
)

# Feature instance & Video features
chat_client = stream_client.chat
video_client = stream_client.video


def create_stream_token(
    user_id: str,
) -> str:
    """
    Create a JWT for authenticating a user with Stream.
    """
    # The unified client has a create_token method
    return stream_client.create_token(user_id)


# Upsert Stream User
async def upsert_stream_user(
    user: User,
) -> None:
    """
    Create or update a user in Stream.
    """

    request = UserRequest(
        id=user.clerk_id,
        name=user.name,
        image=user.profile_image or "",
        role="user",
    )

    stream_client.upsert_users(request)

    logger.info(
        "Stream user synchronized: %s",
        user.clerk_id,
    )


# Delete Stream user
def get_chat_channel(
    channel_id: str,
):
    return chat_client.channel(
        "messaging",
        channel_id,
    )


def get_video_call(
    call_id: str,
):
    return video_client.call(
        "default",
        call_id,
    )
