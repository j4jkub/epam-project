from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str | None = None
    password: str
    repeat_password: str


class UserResponse(BaseModel):
    id: int
    username: str

class AuthenticatedUser(BaseModel):
    id: int
    username: str

