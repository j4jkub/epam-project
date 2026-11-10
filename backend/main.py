from fastapi import FastAPI
# from routers.document_router import document_router
# from routers.project_router import project_router
from .routers.user_router import user_router
from .routers.project_router import project_router
from .db.database import engine, Base
from .models import user
from .models import project


app = FastAPI()
# app.include_router(document_router)
app.include_router(project_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)