import os

from sqlalchemy import ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column

from backend.dependencies.database import Base


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[ForeignKey] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=False)
    content_type: Mapped[str] = mapped_column()


@event.listens_for(Document, "after_delete")
def delete_document_file(mapper, connection, target):
    if target.file_path and os.path.exists(target.file_path):
        os.remove(target.file_path)