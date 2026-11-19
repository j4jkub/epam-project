
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.community.postgres import PostgresContainer

from backend.dependencies.database import Base, get_db
from backend.main import app as fastapi_app
from backend.models.document import Document
from backend.models.project import Project


@pytest.fixture(scope="session")
def postgres():
    with PostgresContainer("postgres:16") as container:
        yield container


@pytest.fixture(scope="session")
def test_engine(postgres):
    engine = create_engine(postgres.get_connection_url())

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def app(db_session):
    def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    yield fastapi_app

    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def test_client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_project(db_session):
    project = Project(
        name=f"test-project-{uuid.uuid4().hex[:8]}",
        description="test"
    )

    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)

    return project

@pytest.fixture
def test_document(test_project, db_session):
    document = Document(
        project_id = test_project.id,
        filename = 'test',
        file_path = 'uploads/test',
        content_type = 'img/jpeg'
    )


    db_session.add(document)
    db_session.commit()
    db_session.refresh(document)

    return document
