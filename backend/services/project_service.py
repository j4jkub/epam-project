from fastapi import HTTPException, Response
from sqlalchemy.orm import Session

from backend.models.project import Project
from backend.models.user import AccessType, ProjectAccess
from backend.repositories.project_access_repository import ProjectAccessRepository
from backend.repositories.project_repository import ProjectRepository
from backend.repositories.user_repository import UserRepository
from backend.schemas.project_schema import (
    ProjectCreate,
    ProjectDetailsResponse,
    ProjectUpdate,
)
from backend.schemas.user_schema import UserResponse


class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository()
        self.project_access_repository = ProjectAccessRepository()
        self.user_repository = UserRepository()

    def create(self, user, project : ProjectCreate, db : Session):
        if self.project_repository.get_by_name(project.name, db):
            raise HTTPException(status_code=400, detail="Project with this name allready exists")

        new_project = Project(
            name = project.name,
            description = project.description
        )
        new_project = self.project_repository.create(new_project, db)

        project_access = ProjectAccess(
            project_id = new_project.id,
            user_id = user.id,
            access_type = AccessType.OWNER
        )
        
        self.project_repository.create_project_access(project_access, db)

        return ProjectDetailsResponse(
            id=new_project.id,
            name=new_project.name,
            description=new_project.description,
            is_owner=True
        )

    def get_project_info(self, authicated_user: UserResponse, project_id: int, db : Session):
        project = self.project_repository.get_by_id(project_id, db)
        owner = self.project_repository.get_owner(project_id, db)
        participants = self.project_repository.get_participants(project_id, db)

        return ProjectDetailsResponse(
            id = project.id,
            name=project.name,
            description=project.description,
            owner=(
                UserResponse(id=owner.id, username=owner.username)
                if owner
                else UserResponse(id=-1, username="[deleted]")
            ),
            participants=[
                UserResponse(id=u.id, username=u.username)
                for u in participants
            ],
            is_owner=owner.id==authicated_user.id
        )

    def update_project(
        self, project_id: int,
        project : ProjectUpdate,
        authenticated_user : UserResponse,
        db : Session
    ):
        if not self.project_repository.get_by_id(project_id, db=db):
            raise HTTPException(404, "Project not found")
        
        project = self.project_repository.update(project_id, project, db)

        return ProjectDetailsResponse(
            id = project.id,
            name = project.name,
            description = project.description
        )

    def list_user_projects_info(self, user, db : Session) -> list[ProjectDetailsResponse]:
        projects = self.project_repository.get_list(user_id=user.id, db=db)
        responses = []

        for p in projects:
            owner = self.project_repository.get_owner(p.id, db)
            participants = self.project_repository.get_participants(p.id, db)

            responses.append(
                ProjectDetailsResponse(
                    id=p.id,
                    name=p.name,
                    description=p.description,
                    owner=(
                        UserResponse(id=owner.id, username=owner.username)
                        if owner
                        else UserResponse(id=-1, username="[deleted]")
                    ),
                    participants=[
                        UserResponse(id=u.id, username=u.username)
                        for u in participants
                    ],
                    is_owner=owner.id==user.id
                )
            )
        return responses
 
    def list_owned_projects(self, user, db : Session) -> list[ProjectDetailsResponse]:
        projects = self.project_repository.get_list(user.id, access_type=AccessType.OWNER ,db=db)
        return [ProjectDetailsResponse(id=p.id, name=p.name, description=p.description) for p in projects]

    def add_participant(
        self,
        project_id : int,
        user: str,
        db: Session,
    ) -> Response:
        user = self.user_repository.get_by_username(
            username = user,
            db = db
        )
        if not user:
            raise HTTPException(404, "User not found")
        
        access = self.project_access_repository.get_user_access(
            project_id = project_id, 
            user_id = user.id,
            db = db
        )

        if access:
            raise HTTPException(404, "User already has access")

        
        project_access = ProjectAccess(
            user_id = user.id,
            project_id = project_id,
            access_type = AccessType.PARTICIPANT
        )
        self.project_access_repository.create(project_access, db)
        return Response(status_code=201, content="Access created")

    def remove_participant(
        self,
        atuhenticated_user,
        atuhenticated_user_access,
        project_id : int,
        username : str,
        db: Session,
    ) -> Response:
        user = self.user_repository.get_by_username(username, db)

        if not user:
            raise HTTPException(404, "User not found")

        acces_to_remove = self.project_access_repository.get_user_access(
            project_id=project_id,
            user_id=user.id,
            db=db
        )

        if not acces_to_remove:
            raise HTTPException(404, "User does not have access to this project")

        if user.id != atuhenticated_user.id and atuhenticated_user == AccessType.PARTICIPANT:
            raise HTTPException(402, "You are not allowed to remove other users")
        
        self.project_access_repository.delete(
            access=acces_to_remove,
            db=db
        )

        return Response(status_code=200, content="User access removed")

    def delete(self, user, project_id, db: Session) -> Response:
        self.project_repository.delete(project_id, db)
        return Response(status_code=200, content="Project deleted")
