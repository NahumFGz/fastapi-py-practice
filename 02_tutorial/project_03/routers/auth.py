from fastapi import APIRouter

router = APIRouter(tags=["Auth"])


@router.get("/")
async def get_user():
    return {"user": "authenticated"}
