from backend.dependencies.database import db_dependency
from backend.models.project import Project
from backend.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectDetailsResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException
from backend.models.user import User, ProjectAccess, AccessType


class ProjectRepository:
    def create(self, project: ProjectCreate, db: Session) -> Project:

        
        new_project = Project(
            name = project.name,
            description = project.description
        )

        db.add(new_project)
        db.commit()
        
        return new_project

    def delete(self, project_id: int, db: Session):
        project = db.scalars(
            select(Project).where(Project.id == project_id)
        ).one_or_none()

        if project is None:
            raise HTTPException(status_code=404, detail="User not found")


        db.delete(project)
        db.commit()



    def get_owner(self, project_id : int, db : Session) -> User:
        return db.query(User).join(ProjectAccess, ProjectAccess.user_id == User.id).filter(
            ProjectAccess.project_id == project_id,
            ProjectAccess.access_type == AccessType.OWNER
        ).first()

    def get_participants(self, project_id : int, db : Session) -> list[User]:
        return db.query(User).join(ProjectAccess, ProjectAccess.user_id == User.id).filter(
            ProjectAccess.project_id == project_id,
            ProjectAccess.access_type == AccessType.PARTICIPANT
        ).all()

    def update(self, project_update: ProjectUpdate, db: Session) -> Project:
        project = db.scalar(
            select(Project).where(Project.id == project_update.id)
        )

        project.name = project_update if project_update.name is not None else project.name
        project.description = project_update if project_update.description is not None else project.name

        db.commit()

        return project


    def get_by_id(self, id: int, db: Session) -> Project:
        return db.scalar(
            select(Project).where(Project.id == id)
        )

    def get_by_name(self, name: str, db: Session) -> Project | None:
        return db.query(Project).filter(Project.name == name).first()

    def get_list(self, user_id : int, db: Session, access_type : AccessType | None = None) -> list[Project]:
        projects_access = db.query(ProjectAccess).filter(ProjectAccess.user_id == user_id)

        if access_type is not None:
            projects_access = projects_access.filter(ProjectAccess.access_type == access_type)


        projects_ids = [p.project_id for p in projects_access.all()]
        projects = db.query(Project).filter(Project.id.in_(projects_ids)).all()

        return projects
        
    def create_project_access(self, user_id, project_id, access_type : AccessType, db: Session) -> ProjectAccess:
        current_access =  db.query(ProjectAccess).filter(ProjectAccess.project_id == project_id, ProjectAccess.user_id == user_id).first()
        if current_access:
            return Response('Access already exists', 401)
        
        project_access = ProjectAccess(
            project_id = project_id,
            user_id = user_id,
            access_type = access_type
        )

        db.add(project_access)
        db.commit()
        
        return project_access