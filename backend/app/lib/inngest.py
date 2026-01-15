from inngest import Inngest, Context, TriggerEvent
from datetime import datetime, timezone
from beanie.operators import Set

from app.models import User
from app.lib.db import connect_db

inngest_client = Inngest(
    app_id="farm-talent-iq",
)


@inngest_client.create_function(
    fn_id="sync-user", trigger=TriggerEvent(event="clerk/user.created")
)
async def sync_user(ctx: Context):
    async def save_user():
        await connect_db()
        data = ctx.event.data

        email = data["email_addresses"][0]["email_address"]
        first = data.get("first_name", "")
        last = data.get("last_name", "")
        name = f"{first} {last}".strip() or email.split("@")[0]

        # Use find_one + upsert
        # This checks for the ID, and if found, updates the fields inside Set()
        # If NOT found, it creates a new record using the on_insert Document
        await User.find_one(User.clerk_id == data["id"]).upsert(
            Set(
                {
                    User.email: email,
                    User.name: name,
                    User.profile_image: data.get("image_url", ""),
                    User.updated_at: datetime.now(timezone.utc),
                }
            ),
            on_insert=User(
                clerk_id=data["id"],
                email=email,
                name=name,
                profile_image=data.get("image_url", ""),
            ),
        )
        return {"status": "success", "user_id": data["id"]}

    await ctx.step.run("upsert-user-to-db", save_user)


@inngest_client.create_function(
    fn_id="delete-user-from-db", trigger=TriggerEvent(event="clerk/user.deleted")
)
async def delete_user(ctx: Context):
    async def remove_user():
        await connect_db()
        clerk_id = ctx.event.data["id"]  # Access as attribute
        user = await User.find_one(User.clerk_id == clerk_id)
        if user:
            await user.delete()
            return True
        return False

    await ctx.step.run("delete-user-db-op", remove_user)
