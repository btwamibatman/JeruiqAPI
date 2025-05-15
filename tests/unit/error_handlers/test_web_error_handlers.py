import pytest
from flask import Flask
from adapters.error_handlers.web_error_handlers import register_error_handlers  # Adjust import

@pytest.fixture
def app():
    app = Flask(__name__)
    register_error_handlers(app)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_404_error(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json == {"error": "Not Found"}

def test_500_error(client, mocker):
    mocker.patch("adapters.error_handlers.web_error_handlers.some_function", side_effect=Exception("Server error"))
    response = client.get("/error")
    assert response.status_code == 500
    assert response.json == {"error": "Internal Server Error"}