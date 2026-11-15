from backend.models.document import Document
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Select

class DocumentRepository:
    def create(self, document: Document, db: Session) -> Document:
        db.add(document)
        db.commit()
        return document

    def delete(self,document: Document, db: Session) -> Document:
        db.delete(document)
        db.commit()
        return document

    def get_project_documents_list(self, project_id : int, db: Session) -> list[Document]:
        return db.scalars(
            Select(Document).where(Document.project_id == project_id)
        )

    def get_by_id(self, document_id, db: Session) -> Document:
        return db.scalar(
            Select(Document).where(Document.id == document_id)
        )


