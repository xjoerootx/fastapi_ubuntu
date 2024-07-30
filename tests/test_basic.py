from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

@pytest.fixture
def mock_session():
    return MagicMock()

def test_add_date(mock_session):
    with patch("database.Documents",
               return_value=MagicMock(id=1, path="test/path", date="2024-07-30")) as mock_document:
        with patch("async_session.new_session", return_value=mock_session):
            # Настраиваем мок для сессии
            mock_session.add = MagicMock()
            mock_session.flush = MagicMock()
            mock_session.commit = MagicMock()

            response = client.post("/table/add_date/", json={"path": "test/path", "date": "2024-07-30"})

    assert response.status_code == 200
    assert response.json() == {"ok": True, "date_id": 1}
    mock_document.assert_called_once_with(path="test/path", date="2024-07-30")


def test_get_dates(mock_session):
    mock_documents = [MagicMock(id=1, path="test/path", date="2024-07-30")]

    with patch("async_session.new_session", return_value=mock_session):
        # Настраиваем мок для выполнения запроса
        mock_session.execute = MagicMock(return_value=MagicMock(scalars=MagicMock(return_value=mock_documents)))

        response = client.get("/table/get_date/")

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "path": "test/path", "date": "2024-07-30"}]


def test_get_dates_empty(mock_session):
    with patch("async_session.new_session", return_value=mock_session):
        # Настраиваем мок для выполнения запроса
        mock_session.execute = MagicMock(return_value=MagicMock(scalars=MagicMock(return_value=[])))

        response = client.get("/table/get_date/")

    assert response.status_code == 200
    assert response.json() == []

