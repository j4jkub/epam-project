from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import Annotated
from backend.dependencies.auth import auth_dependency
from backend.dependencies.database import db_dependency
from backend.models.user import User, AccessType
from backend.repositories.project_access_repository import ProjectAccessRepository

def require_project_access(*allowed_roles) -> AccessType:

    def dependency(
        project_id: int,
        db: db_dependency,
        current_user: auth_dependency,
    ):
        access_repository = ProjectAccessRepository()

        access = access_repository.get_user_access(
            project_id=project_id,
            user_id=current_user.id,
            db=db
        )

        if not access:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this project",
            )

        if access.access_type not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action",
            )

        return access.access_type

    return dependency

require_project_participant = Annotated[AccessType,  Depends(require_project_access(
    AccessType.OWNER,
    AccessType.PARTICIPANT,
))]

require_project_owner = Annotated[AccessType, Depends(require_project_access(
    AccessType.OWNER,
))]