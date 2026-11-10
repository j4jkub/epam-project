from backend.db.database import db_dependency
from backend.models.user import User
from backend.schemas.user_schema import UserCreate
from fastapi import Response

class UserService:
    def does_user_exist(self, username, db : db_dependency) -> bool:
        if db.query(User).filter(username=username).first():
            return True
        return False

    def create_user(self, user : UserCreate, db : db_dependency):
        if self.does_user_exist(user.username, db):
            return Response()
        new_user = User(
            username = user.username,
            email = user.email
        )
        db.add(new_user)
        db.commit
        return Response(new_user, 200)
