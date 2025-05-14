import pytest
from flask import Flask
from domain.services.ai_service.routes.chat_routes import chat_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(chat_bp, url_prefix="/chat")
    return app.test_client()

def test_chat_endpoint(mock_gemini_client, client):
    response = client.post(
        "/chat",
        json={"message": "Hello"},
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 200
    assert response.json == {"response": "Mocked AI response"}
    mock_gemini_client.return_value.generate_content.assert_called_with("Hello")

def test_chat_invalid_message(client):
    response = client.post(
        "/chat",
        json={"message": ""},
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 400
    assert response.json == {"error": "Message cannot be empty"}