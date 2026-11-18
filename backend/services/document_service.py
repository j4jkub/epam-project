from backend.repositories.document_repository import DocumentRepository
from backend.repositories.project_repository import ProjectRepository
from backend.models.document import Document
from backend.schemas.document_schema import DocumentResponse

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
import os
import shutil

class DocumentService:
    def __init__(self):
        self.UPLOAD_PATH = 'uploads'
        self.MAX_FILE_SIZE = 50 * 1024 * 1024
        self.document_repository = DocumentRepository()
        self.project_repository = ProjectRepository()
            
    def upload_file(self, project_id : int, file : UploadFile, db : Session):
        if file.size >  self.MAX_FILE_SIZE:
            raise HTTPException(422, "File is too big")

        project = self.project_repository.get_by_id(
            id=project_id,
            db=db
        )

        if not project: 
            raise HTTPException(404, "Project not found")


        filename = project.name + file.filename
        dir_path = os.path.join(self.UPLOAD_PATH, project.name)
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(
            dir_path,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document = Document(
            project_id = project_id,
            filename = filename,
            file_path = file_path,
            content_type = file.content_type
        )

        return self.document_repository.create(document, db)

    def update_file(self, document_id: int, file : UploadFile, db: Session):
        document = self.document_repository.get_by_id(
            document_id=document_id,
            db=db
        )

        project = self.project_repository.get_by_id(
            id=document.project_id,
            db=db
        )

        if not project: 
            return HTTPException(404, "Project not found")

        filename = project.name + file.filename
        dir_path = os.path.join(self.UPLOAD_PATH, project.name)
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(
            dir_path,
            filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        document

    def delete_file(
            self,
            document_id: int,
            db: Session
    ):
        document = self.document_repository.get_by_id(
            document_id = document_id,
            db = db
        )

        if not document or document.project_id != document.project_id:
            raise HTTPException(404, "File not found")

        self.document_repository.delete(
            document = document,
            db = db
        )

        # if document.file_path and os.path.exists(document.file_path):
        #     os.remove(document.file_path)

        return document

    def download_project_file(self, document_id: int, db: Session):
        document = self.document_repository.get_by_id(
            document_id = document_id,
            db = db
        )
        if not document :
            raise HTTPException(404, "File not found")

        return FileResponse(
            path=document.file_path,
            filename=document.filename,
            media_type=document.content_type
        )

    def get_project_files(self, project_id, db : Session) -> list[DocumentResponse]:
        documents = self.document_repository.get_project_documents_list(
            project_id=project_id,
            db=db
        )
        return [
            DocumentResponse(
                id=d.id,
                filename=d.filename,
                content_type=d.content_type
            ) for d in documents
        ]