import pytest
from flask import Flask
from domain.services.ai_service.routes.session_routes import session_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(session_bp, url_prefix="/session")
    return app.test_client()

def test_create_session(client, mocker):
    mocker.patch(
        "domain.services.ai_service.routes.session_routes.chat_service.create_session",
        return_value={"session_id": "123"}
    )
    response = client.post(
        "/session",
        json={"user_id": 1},
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 201
    assert response.json == {"session_id": "123"}

def test_create_session_unauthorized(client):
    response = client.post("/session", json={"user_id": 1})
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}