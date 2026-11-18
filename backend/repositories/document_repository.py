from backend.models.document import Document
from backend.schemas.document_schema import DocumentUpdate
from fastapi import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import Select

class DocumentRepository:
    def create(self, document: Document, db: Session) -> Document:
        db.add(document)
        db.commit()
        return document

    def delete(self, document: Document, db: Session) -> Document:
        db.delete(document)
        db.commit()
        return document

    def update(self, document_id: int, document_update: Document, db: Session) -> Document:
        document = self.get_by_id(document_id=document_id, db=db)

        if not document:
            return None

        update_data = document_update.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(document, key, value)

        db.flush()
        db.refresh(document)

        return document

    def get_project_documents_list(self, project_id : int, db: Session) -> list[Document]:
        return db.scalars(
            Select(Document).where(Document.project_id == project_id)
        )

    def get_by_id(self, document_id: int, db: Session) -> Document:
        return db.scalar(
            Select(Document).where(Document.id == document_id)
        )


