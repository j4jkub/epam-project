from fastapi import APIRouter
from backend.db.database import db_dependency
from backend.services.project_service import ProjectService
from backend.schemas.project_schema import ProjectCreate
from backend.services.project_service import ProjectService

project_router = APIRouter()
project_service = ProjectService()


@project_router.post("/projects")
def create_project(project : ProjectCreate, db: db_dependency):
    return project_service.create_project(project=project, db=db)

@project_router.get("/project")
def get_all_projects(db: db_dependency):
    pass

@project_router.get("/project/{project_id}/info")
def get_project_info(project_id, db: db_dependency):
    pass

@project_router.put("/project/{project_id}/info")
def update_project_info(project_id, db: db_dependency):
    pass

@project_router.delete("/project/{project_id}")
def delete_project(project_id, db: db_dependency):
    pass

@project_router.get("/project/{project_id}/documents")
def get_project_documents(project_id, db: db_dependency):
    pass

@project_router.post("/project/{project_id}/")
def invite_user_to_project(project_id, user, db: db_dependency):
    pass

@project_router.get("/project/{project_id}/")
def send_project_email_invite(project_id, user, db: db_dependency):
    pass