import email

from fastapi import APIRouter
from models import Users
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    last_name: str
    password: str
    role: str


@router.get("/")
async def get_user():
    return {"user": "authenticated"}


@router.post("/")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request.password,
        is_active=True,
    )

    return create_user_model
