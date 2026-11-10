from backend.db.database import db_dependency
from backend.models.project import Project
from backend.schemas.project_schema import ProjectCreate
from fastapi import Response
from sqlalchemy.orm import Session
from backend.repositories.project_repository import ProjectRepository

class ProjectService:
    def __init__(self):
        self.project_repository = ProjectRepository()

    def create_project(self, project : ProjectCreate, db : Session):
        return self.project_repository.create(project, db)

        