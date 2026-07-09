from fastapi import FastAPI
from inngest import Context, Inngest, TriggerEvent
from inngest.fast_api import serve

from app.core.config import settings
from app.core.db import connect_db
from app.core.logger import logger
from app.repositories.user import (
    delete,
    get_by_clerk_id,
    upsert_from_clerk,
)

inngest_client = Inngest(
    app_id="farm-talent-iq",
    signing_key=settings.INNGEST_SIGNING_KEY,
    event_key=settings.INNGEST_EVENT_KEY,
)


@inngest_client.create_function(
    fn_id="sync-user",
    trigger=TriggerEvent(
        event="clerk/user.created",
    ),
)
async def sync_user(
    ctx: Context,
) -> None:
    async def save_user() -> dict[str, str]:
        await connect_db()

        data = ctx.event.data

        email = data["email_addresses"][0]["email_address"]

        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")

        name = f"{first_name} {last_name}".strip() or email.split("@")[0]

        await upsert_from_clerk(
            clerk_id=data["id"],
            email=email,
            name=name,
            profile_image=data.get("image_url", ""),
        )

        logger.info(
            "User %s synchronized from Clerk.",
            data["id"],
        )

        return {
            "status": "success",
            "user_id": data["id"],
        }

    await ctx.step.run(
        "upsert-user-to-db",
        save_user,
    )


@inngest_client.create_function(
    fn_id="delete-user",
    trigger=TriggerEvent(event="clerk/user.deleted"),
)
async def delete_user(
    ctx: Context,
) -> None:
    async def remove_user() -> bool:
        await connect_db()

        clerk_id = ctx.event.data["id"]

        user = await get_by_clerk_id(clerk_id)

        if user is None:
            logger.warning(
                "User %s not found during delete event.",
                clerk_id,
            )
            return False

        await delete(user)

        logger.info(
            "User %s deleted.",
            clerk_id,
        )

        return True

    await ctx.step.run(
        "delete-user-from-db",
        remove_user,
    )


def register_inngest(
    app: FastAPI,
) -> None:
    """
    Inngest Serve - Registering functions at /api/inngest
    The SDK automatically handles the POST and GET handshakes
    """
    serve(
        app,
        inngest_client,
        [
            sync_user,
            delete_user,
        ],
        serve_path="/api/inngest",
    )
