import pytest
from flask import Flask
from api_gateway.routes.auth_routes import auth_bp  # Adjust import

@pytest.fixture
def client(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app.test_client()

def test_login_success(client, mocker):
    mocker.patch(
        "api_gateway.routes.auth_routes.user_login.execute",
        return_value="jwt_token"
    )
    response = client.post("/auth/login", json={"username": "testuser", "password": "password"})
    
    assert response.status_code == 200
    assert response.json == {"token": "jwt_token"}

def test_login_invalid_credentials(client, mocker):
    mocker.patch(
        "api_gateway.routes.auth_routes.user_login.execute",
        side_effect=ValueError("Invalid credentials")
    )
    response = client.post("/auth/login", json={"username": "testuser", "password": "wrong"})
    
    assert response.status_code == 401
    assert response.json == {"error": "Invalid credentials"}