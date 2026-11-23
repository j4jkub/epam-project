import os
import re
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.core.storage import s3, BUCKET
from backend.models.document import Document
from backend.repositories.document_repository import DocumentRepository
from backend.repositories.project_repository import ProjectRepository
from backend.schemas.document_schema import DocumentResponse



def _safe_name(name: str) -> str:
    name = os.path.basename(name or "file")
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


class DocumentService:
    MAX_FILE_SIZE = 50 * 1024 * 1024

    def __init__(self):
        self.document_repository = DocumentRepository()
        self.project_repository = ProjectRepository()

    def _check_size(self, file: UploadFile):
        # file.size can be None, so measure the stream instead
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
        if size > self.MAX_FILE_SIZE:
            raise HTTPException(422, "File is too big")

    def _put(self, project_id: int, file: UploadFile) -> tuple[str, str]:
        filename = _safe_name(file.filename)
        key = f"projects/{project_id}/{uuid.uuid4().hex}-{filename}"
        s3.upload_fileobj(
            file.file, BUCKET, key,
            ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
        )
        return key, filename

    def upload_file(self, project_id: int, file: UploadFile, db: Session):
        self._check_size(file)

        project = self.project_repository.get_by_id(id=project_id, db=db)
        if not project:
            raise HTTPException(404, "Project not found")

        key, filename = self._put(project_id, file)

        document = Document(
            project_id=project_id,
            filename=filename,
            file_path=key,                 # now holds the S3 key
            content_type=file.content_type,
        )
        try:
            return self.document_repository.create(document, db)
        except Exception:
            s3.delete_object(Bucket=BUCKET, Key=key)   # no orphan if DB fails
            raise

    def update_file(self, document_id: int, file: UploadFile, db: Session):
        self._check_size(file)

        document = self.document_repository.get_by_id(document_id=document_id, db=db)
        if not document:
            raise HTTPException(404, "Document not found")

        old_key = document.file_path
        key, filename = self._put(document.project_id, file)

        document.filename = filename
        document.file_path = key
        document.content_type = file.content_type
        db.commit()
        db.refresh(document)

        s3.delete_object(Bucket=BUCKET, Key=old_key)
        return document

    def delete_file(self, document_id: int, db: Session):
        document = self.document_repository.get_by_id(document_id=document_id, db=db)
        if not document:
            raise HTTPException(404, "File not found")

        key = document.file_path
        self.document_repository.delete(document=document, db=db)
        s3.delete_object(Bucket=BUCKET, Key=key)
        return document

    def download_project_file(self, document_id: int, db: Session):
        document = self.document_repository.get_by_id(document_id=document_id, db=db)
        if not document:
            raise HTTPException(404, "File not found")

        try:
            obj = s3.get_object(Bucket=BUCKET, Key=document.file_path)
        except s3.exceptions.NoSuchKey:
            raise HTTPException(404, "File missing from storage")

        return StreamingResponse(
            obj["Body"].iter_chunks(1024 * 64),
            media_type=document.content_type or "application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{document.filename}"'},
        )

    def get_project_files(self, project_id, db: Session) -> list[DocumentResponse]:
        documents = self.document_repository.get_project_documents_list(
            project_id=project_id, db=db
        )
        return [
            DocumentResponse(id=d.id, filename=d.filename, content_type=d.content_type)
            for d in documents
        ]