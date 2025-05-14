import pytest
from flask import Flask
from api_gateway.routes.user_routes import user_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(user_bp, url_prefix="/users")
    return app.test_client()

def test_create_user(client, mocker):
    mocker.patch(
        "api_gateway.routes.user_routes.user_registration.execute",
        return_value={"id": 1, "username": "testuser", "email": "test@example.com"}
    )
    response = client.post(
        "/users",
        json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )
    
    assert response.status_code == 201
    assert response.json["username"] == "testuser"

def test_create_user_invalid_email(client):
    response = client.post(
        "/users",
        json={"username": "testuser", "email": "invalid", "password": "password"}
    )
    
    assert response.status_code == 400
    assert "error" in response.json