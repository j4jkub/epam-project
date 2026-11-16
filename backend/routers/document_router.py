from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse, Response

from backend.schemas.document_schema import DocumentResponse
from backend.services.document_service import DocumentService
from backend.dependencies.auth import auth_dependency
from backend.dependencies.database import db_dependency
from backend.dependencies.project_access import require_project_owner, require_project_participant

document_router = APIRouter()
document_service = DocumentService()


@document_router.get("/document/{document_id}")
def download_document(
    document_id: int,
    authicated_user: auth_dependency,
    db:db_dependency
) -> FileResponse:
    return document_service.download_project_file(
        document_id=document_id,
        db=db
    )

@document_router.put("/document/{document_id}")
def update_document(document_id) -> DocumentResponse:
    pass

@document_router.post("/project/{project_id}/documents")
async def add_project_document(
    project_id,
    file: UploadFile,
    authicated_user: auth_dependency,
    db: db_dependency,
    access = require_project_participant
) -> DocumentResponse:
    return document_service.upload_file(
        project_id=project_id,
        file=file,
        db=db
    )

@document_router.delete("/project/{project_id}/documents")
async def delete_project_document(
    project_id,
    file: UploadFile,
    authicated_user: auth_dependency,
    db: db_dependency,
    access = require_project_participant
) -> Response:
    document_service.upload_file(
        project_id=project_id,
        file=file,
        db=db
    )
    return Response(status_code=201, content="File created ")

@document_router.get("/project/{project_id}/documents")
def get_project_documents(
    project_id,
    authicated_user: auth_dependency,
    db: db_dependency,
    access = require_project_participant
) -> list[DocumentResponse]:
    return document_service.get_project_files(
        project_id=project_id,
        db=db
        )

