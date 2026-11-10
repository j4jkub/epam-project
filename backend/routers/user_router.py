from fastapi import APIRouter, Response
from backend.db.database import db_dependency
from backend.schemas.user_schema import UserCreate
from backend.services.user_service import UserService

user_router = APIRouter()

@user_router.post("/auth")
def create_user(user : UserCreate, db: db_dependency):
    if UserService.does_user_exist(user.username):
        return Response("Username already exists", 401)
    
    UserService.create_user(user, db)
    return Response("User Created", 200)


@user_router.post("/login")
def login_user(db: db_dependency):
    pass

@user_router.get("/user/{username}")
def get_user(username, db: db_dependency):
    pass
