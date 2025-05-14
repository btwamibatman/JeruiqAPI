import pytest
from flask import Flask
from infrastructure.db.session import SessionLocal
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret"
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session():
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def mock_gemini_client():
    with patch("google.generativeai.GenerativeModel") as mock:
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value = {"text": "Mocked AI response"}
        mock.return_value = mock_instance
        yield mock

@pytest.fixture
def mock_requests():
    with patch("requests.post") as mock:
        mock.return_value.json.return_value = {"response": "Mocked service response"}
        mock.return_value.status_code = 200
        yield mock