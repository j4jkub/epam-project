from fastapi import APIRouter

user_router = APIRouter()

@user_router.post("/auth")
def create_user():
    pass

@user_router.post("/login")
def login_user():
    pass