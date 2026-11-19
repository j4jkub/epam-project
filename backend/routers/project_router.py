from fastapi import APIRouter, Response

from backend.dependencies.auth import auth_dependency
from backend.dependencies.database import db_dependency
from backend.dependencies.project_access import (
    require_project_owner,
    require_project_participant,
)
from backend.schemas.project_schema import (
    ProjectCreate,
    ProjectDetailsResponse,
    ProjectUpdate,
)
from backend.services.project_service import ProjectService
from backend.services.user_service import UserService

project_router = APIRouter()
project_service = ProjectService()
user_service = UserService()


@project_router.post("/projects")
def create_project(project : ProjectCreate, authicated_user: auth_dependency, db: db_dependency) -> ProjectDetailsResponse:
    return project_service.create(project=project, db=db, user=authicated_user)

@project_router.get("/projects")
def get_all_projects(authicated_user: auth_dependency, db: db_dependency) -> list[ProjectDetailsResponse]:
    return project_service.list_user_projects_info(authicated_user, db)

@project_router.get("/project/{project_id}/info")
def get_project_info(
    project_id: int,
    access: require_project_participant,
    authicated_user: auth_dependency,
    db: db_dependency,
    ) -> ProjectDetailsResponse:
    return project_service.get_project_info(authicated_user, project_id, db)

@project_router.put("/project/{project_id}/info")
def update_project_info(
    project_id: int,
    project_update: ProjectUpdate,
    access: require_project_participant,
    authicated_user: auth_dependency,
    db: db_dependency,
) -> ProjectDetailsResponse:
    return project_service.update_project(project_id, project_update, authicated_user , db)
    

@project_router.delete("/project/{project_id}")
def delete_project(
    project_id: int,
    authicated_user: auth_dependency,
    db: db_dependency,
    access: require_project_owner
) -> Response:
    return project_service.delete(authicated_user, project_id, db)


@project_router.post("/project/{project_id}/invite")
def invite_user_to_project(
    project_id: int,
    user: str,
    authicated_user: auth_dependency,
    db: db_dependency,
    access: require_project_owner
) -> Response:
    return project_service.add_participant(
        project_id=project_id,
        user=user,
        db=db
    )

@project_router.delete("/project/{project_id}/invite")
def remove_participant_from_project(
    project_id: int,
    user: str,
    authicated_user: auth_dependency,
    db: db_dependency,
    access: require_project_participant
) -> Response:
    return project_service.remove_participant(
        project_id=project_id,
        username=user,
        atuhenticated_user_access=access,
        atuhenticated_user=authicated_user,
        db=db
    )

@project_router.get("/project/{project_id}/")
def send_project_email_invite(
    project_id: int,
    username,
    authicated_user: auth_dependency,
    db: db_dependency,
    access: require_project_participant
):
    pass