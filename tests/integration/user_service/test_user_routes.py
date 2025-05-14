import pytest
from flask import Flask
from domain.services.user_service.routes.user_routes import user_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(user_bp, url_prefix="/users")
    return app.test_client()

def test_get_user(client, mocker):
    mocker.patch(
        "domain.services.user_service.routes.user_routes.user_service.get_user",
        return_value={"id": 1, "username": "testuser", "email": "test@example.com"}
    )
    response = client.get(
        "/users/1",
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 200
    assert response.json["username"] == "testuser"

def test_get_user_unauthorized(client):
    response = client.get("/users/1")
    assert response.status_code == 401
    assert response.json == {"error": "Unauthorized"}