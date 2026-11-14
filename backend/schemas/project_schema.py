from pydantic import BaseModel
from backend.schemas.user_schema import UserResponse

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class ProjectDetailsResponse(BaseModel):
    id: int
    name: str
    description: str
    owner: UserResponse | None = None
    participants: list[UserResponse] | None = None
    is_owner: bool | None = None

class ProjectAccessRequest(BaseModel):
    username: str
    project_id: int