from datetime import UTC, datetime

from beanie.operators import Set

from app.models.user import User


async def get_by_clerk_id(
    clerk_id: str,
) -> User | None:
    return await User.find_one(
        User.clerk_id == clerk_id,
    )


async def upsert_from_clerk(
    *,
    clerk_id: str,
    email: str,
    name: str,
    profile_image: str,
) -> None:
    await User.find_one(
        User.clerk_id == clerk_id,
    ).upsert(
        Set(
            {
                User.email: email,
                User.name: name,
                User.profile_image: profile_image,
                User.updated_at: datetime.now(UTC),
            }
        ),
        on_insert=User(
            clerk_id=clerk_id,
            email=email,
            name=name,
            profile_image=profile_image,
        ),
    )


async def delete(
    user: User,
) -> None:
    await user.delete()
