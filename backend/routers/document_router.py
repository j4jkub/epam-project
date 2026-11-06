from fastapi import APIRouter

document_router = APIRouter()

@document_router.get("/document/{document_id}")
def download_document(document_id):
    pass

@document_router.put("/document/{document_id}")
def update_document(document_id):
    pass

@document_router.post("/project/{project_id}/documents")
def add_project_document(project_id):
    pass