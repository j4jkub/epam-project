from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

import jwt

from backend.schemas.token_schema import Token, TokenData
from backend.schemas.user_schema import UserResponse
from backend.dependencies.database import db_dependency
from backend.models.user import User


SECRET_KEY = "3c76d101037cd4047c1b096c26d740a1d1a546a3c6f58ff6e508a0354ea6594b"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
password_hash = PasswordHash.recommended()



def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(username: str, db : db_dependency):
    user = db.query(User).filter(User.username == username).first()
    return user


def authenticate_user(username: str, password: str, db : db_dependency):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : db_dependency):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(username=token_data.username, db=db)
    
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user : Annotated[UserResponse, Depends(get_current_user)],
):
    # if not current_user.is_active:
        # raise HTTPException(status_code=400, detail="Inactive user")
    return UserResponse(
        id=current_user.id,
        username=current_user.username
    )

auth_dependency = Annotated[UserResponse, Depends(get_current_user)]