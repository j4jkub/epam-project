from backend.db.database import db_dependency
from backend.models.project import Project
from backend.schemas.project_schema import ProjectCreate
from sqlalchemy.orm import Session
from fastapi import Response


class ProjectRepository:
    def create(project : ProjectCreate, db : Session):
        new_project = Project(
            name = project.name,
            description = project.description
        )

        db.add(new_project)
        db.commit()

    
    