from datetime import datetime
from backend.dependencies.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[ForeignKey] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    content_type: Mapped[str] = mapped_column()