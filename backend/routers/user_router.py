from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from backend.dependencies.auth import get_current_active_user
from backend.dependencies.database import db_dependency
from backend.schemas.token_schema import Token
from backend.schemas.user_schema import UserCreate, UserResponse
from backend.services.user_service import UserService

user_router = APIRouter()
user_service = UserService()

ACCESS_TOKEN_EXPIRE_MINUTES = 60


@user_router.post("/auth")
async def register_user(user: UserCreate, db : db_dependency) -> Response:
    return user_service.create_user(
        user = user,
        db = db
    )


@user_router.get("/user/{username}")
def get_user(username: str, db: db_dependency) -> UserResponse:
    return user_service.get_user_by_username(username, db)

@user_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db : db_dependency
) -> Token:
    return user_service.get_access_token(
        form_data=form_data,
        db=db
    )

@user_router.get("/auth/me/")
async def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user