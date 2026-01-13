from fastapi import APIRouter, Depends
from app.lib.clerk import verify_clerk_token

router = APIRouter()

@router.get("/")
async def getChats(user=Depends(verify_clerk_token)):
    return {"message": f"Hello {user['sub']}! Here are your chats."}


@router.post("/")
async def createChat(user=Depends(verify_clerk_token), content: str = "default"):
    return {"message": f"Chat created by {user['sub']}", "content": content}
