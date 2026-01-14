from inngest import Inngest, Context, TriggerEvent

from app.models import User
from app.lib.db import connect_db
from .config import settings

inngest_client = Inngest(
    app_id="farm-talent-iq",
)


@inngest_client.create_function(
    fn_id="sync-user", trigger=TriggerEvent(event="clerk/user.created")
)
async def sync_user(ctx: Context):
    # This block is now durable and retriable
    async def save_user():
        await connect_db()
        data = ctx.event.data  # Access as attribute

        email = data["email_addresses"][0]["email_address"]
        name = f'{data.get("first_name","")} {data.get("last_name","")}'.strip()

        user = User(
            clerk_id=data["id"],
            email=email,
            name=name,
            profileImage=data.get("image_url", ""),
        )
        return await user.insert()

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
