from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def homePage():
    return { "message": "Home Page" }