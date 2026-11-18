from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.document_router import document_router
from backend.routers.user_router import user_router
from backend.routers.project_router import project_router
from backend.dependencies.database import engine, Base


app = FastAPI()
app.include_router(prefix="/api", router=document_router, tags=['documents'])
app.include_router(prefix="/api", router=project_router, tags=['project'])
app.include_router(prefix="/api", router=user_router, tags=['users'])



origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
