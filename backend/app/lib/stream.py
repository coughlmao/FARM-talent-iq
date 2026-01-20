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


# Upsert Stream User
async def upsert_stream_user(user_data: dict):
    try:
        client.upsert_users(
            UserRequest(
                id=user_data.get("id"),
                name=user_data.get("name"),
                image=user_data.get("image"),
                role=user_data.get("role", "user"),
            )
        )
        print(f"Stream user upserted successfully:{user_data.get('id')}")
    except Exception as e:
        print(f"Error upserting Stream user:{e}")


# Delete Stream user
async def delete_stream_user(user_id: str):
    try:
        client.users.delete(user_id)
        print(f"Stream user deleted successfully:{user_id}")
    except Exception as e:
        print(f"Error deleting the Stream user: {e}")
