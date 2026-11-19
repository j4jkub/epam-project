import pytest

from backend.models.document import Document
from backend.repositories.document_repository import DocumentRepository


@pytest.fixture
def document_repository():
    return DocumentRepository()


def test_create_and_get_by_id_document(document_repository, test_project, db_session):
    document = Document(
        project_id = test_project.id,
        filename = 'test',
        file_path = 'uploads/test',
        content_type = 'img/jpeg'
    )

    result = document_repository.create(document, db_session)

    assert result.id is not None

    saved_document = document_repository.get_by_id(
        result.id,
        db_session
    )

    assert saved_document is not None

def test_delete_document(document_repository, test_document, db_session):
    document = document_repository.delete(
        document=test_document,
        db=db_session
    )

    assert document_repository.get_by_id(
        document_id=document.id,
        db=db_session
        ) is None