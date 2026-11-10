from pydantic import BaseModel

class UserCreate(BaseModel):
    username : str
    bio : str
    email : str
    password: str
    repeat_password : str

class UserRequest(BaseModel):
    pass
