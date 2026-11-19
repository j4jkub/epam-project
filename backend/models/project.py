from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.dependencies.database import Base


class Project(Base):
    __tablename__ = "projects"
    id : Mapped[int] = mapped_column( primary_key=True, index=True )
    name : Mapped[str] = mapped_column(index=True, unique=True)
    description : Mapped[str] = mapped_column()
    created_at : Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    # documents: Mapped["Document"] = relationship(
    #     back_populates="project",
    # )