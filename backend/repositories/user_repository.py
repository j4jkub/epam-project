from sqlalchemy.orm import Session

from backend.models.user import User


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
    