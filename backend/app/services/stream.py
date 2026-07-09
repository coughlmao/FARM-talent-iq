from app.integrations.stream import (
    chat_client,
    create_stream_token,
    upsert_stream_user,
    video_client,
)
from app.models.user import User


async def ensure_stream_user(user: User) -> None:
    await upsert_stream_user(user)


def build_stream_token(user: User) -> str:
    return create_stream_token(user.clerk_id)


def get_video_call(call_id: str):
    return video_client.call("default", call_id)


def get_chat_channel(call_id: str):
    return chat_client.channel(
        "messaging",
        call_id,
    )
