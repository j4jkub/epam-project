from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from backend.db.database import Base
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class AccessType(enum.Enum):
    OWNER = "owner"
    PARTICIPANT = "participant"

class ProjectAccess(Base):
    __tablename__ = "project_access"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    access_level = Column(SQLEnum(AccessType))
