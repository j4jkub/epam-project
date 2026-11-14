from backend.dependencies.database import db_dependency, get_db
from backend.models.project import Project
from backend.schemas.project_schema import ProjectCreate, ProjectUpdate, ProjectDetailsResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Response, HTTPException
from backend.models.user import User, ProjectAccess, AccessType


class ProjectAccessRepository():

    def get_user_access(
        self,
        project_id: int,
        user_id: int,
        db: Session
    ):
        return (
            db.query(ProjectAccess)
            .filter(
                ProjectAccess.project_id == project_id,
                ProjectAccess.user_id == user_id,
            )
            .first()
        )

    def create(self, access: ProjectAccess, db: Session):
        db.add(access)
        db.commit()
        db.refresh(access)
        return access

    def delete(self, access: ProjectAccess, db : Session):
        db.delete(access)
        db.commit()

    def get_project_members(self, project_id: int, db: Session):
        return (
            self.db.query(ProjectAccess)
            .filter(ProjectAccess.project_id == project_id)
            .all()
        )

