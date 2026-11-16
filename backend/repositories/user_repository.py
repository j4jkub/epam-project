from backend.dependencies.database import db_dependency
from backend.models.user import User
from backend.schemas.user_schema import UserCreate, UserResponse
from sqlalchemy.orm import Session
from fastapi import Response

class UserRepository:
    def create(self, user: User, db: Session):
        db.add(user)
        db.commit()
        return user

    def get_by_id(self, id: int, db: Session):
        user = db.query(User).filter(User.id == id).first()
        return user
    
    def get_by_username(self, username: str, db: Session):
        user = db.query(User).filter(User.username == username).first()
        return user
    