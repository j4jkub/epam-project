from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.dependencies.database import Base, engine
from backend.routers.document_router import document_router
from backend.routers.project_router import project_router
from backend.routers.user_router import user_router
from contextlib import asynccontextmanager

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if engine is not None:                      # skipped in tests, where the fixture creates the tables
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(prefix="/api", router=document_router, tags=['documents'])
app.include_router(prefix="/api", router=project_router, tags=['project'])
app.include_router(prefix="/api", router=user_router, tags=['users'])



origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
    'http://localhost:4566',
    os.getenv("FRONTEND_ORIGIN", "http://localhost:4566")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
