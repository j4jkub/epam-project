from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from backend.dependencies.database import Base
from datetime import datetime
import enum

class User(Base):
    __tablename__ = "users"
    id : Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    username: Mapped[str] = mapped_column( index=True, unique=True )
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column( default=True )
    created_at: Mapped[datetime] = mapped_column( DateTime, default=datetime.now ) 

class AccessType(enum.Enum):
    OWNER = "owner"
    PARTICIPANT = "participant"

class ProjectAccess(Base):
    __tablename__ = "project_access"
    id : Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    user_id : Mapped[int] = mapped_column( ForeignKey( "users.id" ) )
    project_id : Mapped[int] = mapped_column( ForeignKey("projects.id", ondelete="CASCADE") )
    access_type : Mapped[AccessType] = mapped_column( SQLEnum(AccessType) )
