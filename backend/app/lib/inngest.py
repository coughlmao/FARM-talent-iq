from app.models import User

async def sync_user(event:dict):
    data=event["data"]

    user=User(
        clerk_id=data["id"],
        email=data["email_addresses"][0]["email_address"],
        name=f'{data.get("first_name","")}{data.get("last_name","")}'.strip(),
        profileImage=data.get("image_url",""),
    )
    await user.insert()

async def delete_user(event:dict):
    clerk_id=event["data"]["id"]
    user=await User.find_one(User.clerk_id==clerk_id)
    if user:
        await user.delete()