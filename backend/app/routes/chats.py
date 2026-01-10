from fastapi import APIRouter, Depends
from app.depends.clerk import verifyClerkToken

router = APIRouter()

@router.get("/")
async def getChats(user=Depends(verifyClerkToken)):
    return {"message": f"Hello {user['sub']}! Here are your chats."}


@router.post("/")
async def createChat(user=Depends(verifyClerkToken), content: str = "default"):
    return {"message": f"Chat created by {user['sub']}", "content": content}
