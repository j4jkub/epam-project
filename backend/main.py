from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.user_router import user_router
from .routers.project_router import project_router
from .dependencies.database import engine, Base

app = FastAPI()
# app.include_router(document_router)
app.include_router(project_router, tags=['project'])
app.include_router(user_router, tags=['users'])



origins = ['http://localhost:5173', 'https://localhost:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
