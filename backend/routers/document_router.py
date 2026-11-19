from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse, Response

from backend.dependencies.auth import auth_dependency
from backend.dependencies.database import db_dependency
from backend.dependencies.document_access import doc_require_project_participant
from backend.dependencies.project_access import require_project_participant
from backend.schemas.document_schema import DocumentResponse
from backend.services.document_service import DocumentService

document_router = APIRouter()
document_service = DocumentService()


@document_router.get("/document/{document_id}")
def download_document(
    document_id: int,
    access: doc_require_project_participant,
    authicated_user: auth_dependency,
    db:db_dependency
) -> FileResponse:
    return document_service.download_project_file(
        document_id=document_id,
        db=db
    )

@document_router.put("/document/{document_id}")
def update_document(
    document_id: int,
    file: UploadFile,
    access: doc_require_project_participant,
    authicated_user: auth_dependency,
    db:db_dependency
) -> DocumentResponse:
    return document_service.update_file(
        document_id=document_id,
        file=file,
        db=db
    )

@document_router.delete("/document/{document_id}")
async def delete_project_document(
    document_id: int,
    access: doc_require_project_participant,
    authicated_user: auth_dependency,
    db: db_dependency,
) -> Response:
    try:
        document_service.delete_file(
            document_id= document_id,
            db=db
        )
    except Exception:
        db.rollback()
        raise

@document_router.post("/project/{project_id}/documents")
async def add_project_document(
    project_id: int,
    file: UploadFile,
    access: require_project_participant,
    authicated_user: auth_dependency,
    db: db_dependency,
) -> DocumentResponse:
    return document_service.upload_file(
        project_id=project_id,
        file=file,
        db=db
    )


@document_router.get("/project/{project_id}/documents")
def get_project_documents(
    project_id: int,
    access: require_project_participant,
    authicated_user: auth_dependency,
    db: db_dependency,
) -> list[DocumentResponse]:
    return document_service.get_project_files(
        project_id=project_id,
        db=db
        )

