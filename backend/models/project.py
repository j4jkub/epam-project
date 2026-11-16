from sqlalchemy import DateTime
from datetime import datetime
from backend.dependencies.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Project(Base):
    __tablename__ = "projects"
    id : Mapped[int] = mapped_column( primary_key=True, index=True )
    name : Mapped[str] = mapped_column(index=True, unique=True)
    description : Mapped[str] = mapped_column()
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now())