from getstream import Stream
from getstream.models import UserRequest

from .config import settings

# Unified client for both chat and video
client = Stream(
    api_key=settings.STREAM_API_KEY,
    api_secret=settings.STREAM_API_SECRET,
)

# Feature instance
chat_features = client.chat

# Video features
video_features = client.video


def create_stream_token(user_id: str):
    """
    Generates a Stream-specific JWT.
    This is what fixes the 'Token signature is invalid' error.
    """
    # The unified client has a create_token method
    return client.create_token(user_id)


# Upsert Stream User
async def upsert_stream_user(user_data: dict):
    try:
        user_req = UserRequest(
            id=str(user_data.get("id")),
            name=str(user_data.get("name") or "Anonymous"),
            image=str(user_data.get("image") or ""),
            role=user_data.get("role", "user"),
        )
        client.upsert_users(user_req)
        print(f"Stream user upserted successfully:{user_data.get('id')}")
    except Exception as err:
        print(f"Error upserting Stream user:{err}")
        raise err


# Delete Stream user
async def delete_stream_user(user_id: str):
    try:
        client.users.delete(user_id)
        print(f"Stream user deleted successfully:{user_id}")
    except Exception as err:
        print(f"Error deleting the Stream user: {err}")
