from backend.models.user import User
from backend.schemas.user_schema import UserCreate
from backend.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status, APIRouter, Response
from sqlalchemy.orm import Session
from backend.schemas.token_schema import Token
from backend.dependencies.auth import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from backend.schemas.user_schema import UserCreate, UserResponse


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def create_user(self, user: UserCreate, db: Session):
        if user.password != user.repeat_password:
           raise HTTPException(422, "Passwords must match")

        if self.user_repository.get_by_username(
            username=user.username,
            db=db
        ) is not None:
            raise HTTPException(422, "User with this name already exists")
    
        new_user = User(
            username=user.username,
            hashed_password=get_password_hash(user.password),
            is_active=True
        )
        
        return self.user_repository.create(new_user, db)

    def get_access_token(
        self,
        form_data: OAuth2PasswordRequestForm,
        db : Session
    ) -> Token:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        user_response = UserResponse(
            id=user.id,
            username=user.username
        )
        return Token(access_token=access_token, token_type="bearer", user=user_response)

    def get_user_by_id(self, id: int, db : Session):
        return self.user_repository.get_by_id(id, db)

    def get_user_by_username(self, username: str, db: Session):
        return self.user_repository.get_by_username(username, db)
