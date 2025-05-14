import pytest
from flask import Flask
from api_gateway.routes.chat_routes import chat_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(chat_bp, url_prefix="/chat")
    return app.test_client()

def test_chat_endpoint(mock_requests, client):
    response = client.post(
        "/chat",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 200
    assert response.json == {"response": "Mocked service response"}
    mock_requests.assert_called_with(
        "http://ai-service:5000/chat",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer valid_token"}
    )

def test_chat_unauthorized(client):
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}