
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

import os

Base = declarative_base()

URL_DATABASE = os.getenv("URL_DATABASE")

engine = None
SessionLocal = None

if URL_DATABASE:
    engine = create_engine(URL_DATABASE)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


def get_db():
    if SessionLocal is None:
        raise RuntimeError("Database URL is not configured.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
