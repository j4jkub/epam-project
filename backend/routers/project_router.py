from fastapi import APIRouter

project_router = APIRouter()

@project_router.post("/projects")
def create_project():
    pass

@project_router.get("/project")
def get_all_projects():
    pass

@project_router.get("/project/{project_id}/info")
def get_project_info(project_id):
    pass

@project_router.put("/project/{project_id}/info")
def update_project_info(project_id):
    pass

@project_router.delete("/project/{project_id}")
def delete_project(project_id):
    pass

@project_router.get("/project/{project_id}/documents")
def get_project_documents(project_id):
    pass

@project_router.post("/project/{project_id}/")
def invite_user_to_project(project_id, user):
    pass

@project_router.get("/project/{project_id}/")
def send_project_email_invite(project_id, user):
    pass