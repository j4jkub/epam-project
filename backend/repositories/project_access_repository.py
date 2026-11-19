from sqlalchemy.orm import Session

from backend.models.user import ProjectAccess


class ProjectAccessRepository:

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
        return access

    def get_project_members(self, project_id: int, db: Session):
        return (
            db.query(ProjectAccess)
            .filter(ProjectAccess.project_id == project_id)
            .all()
        )

