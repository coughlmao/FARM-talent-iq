from beanie import PydanticObjectId
from beanie.operators import Or

from app.models.session import Session, SessionStatus
from app.models.user import User


async def create(
    session: Session,
) -> Session:
    await session.create()
    return session


async def get_by_id(
    session_id: PydanticObjectId,
) -> Session | None:
    return await Session.get(
        session_id,
        fetch_links=True,
    )


async def list_active() -> list[Session]:
    return (
        await Session.find(
            Session.status == SessionStatus.ACTIVE,
            fetch_links=True,
        )
        .sort("-created_at")
        .limit(20)
        .to_list()
    )


async def list_recent(
    user: User,
) -> list[Session]:
    return (
        await Session.find(
            Session.status == SessionStatus.COMPLETED,
            Or(
                Session.host.id == user.id,
                Session.participant.id == user.id,
            ),
            fetch_links=True,
        )
        .sort("-created_at")
        .limit(20)
        .to_list()
    )


async def save(
    session: Session,
) -> Session:
    await session.save()
    return session
