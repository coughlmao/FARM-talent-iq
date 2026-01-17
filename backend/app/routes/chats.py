from typing import Annotated

from fastapi import APIRouter, Depends

from ..lib.clerk import verify_clerk_token

router = APIRouter()

UserDep = Annotated[dict, Depends(verify_clerk_token)]


@router.get("/")
async def getChats(user: UserDep):
    return {"message": f"Hello {user['sub']}! Here are your chats."}


@router.post("/")
async def createChat(user: UserDep, content: str = "default"):
    return {"message": f"Chat created by {user['sub']}", "content": content}
