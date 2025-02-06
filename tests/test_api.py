import pytest
from main import app

def test_register_user(client):
    """Тест регистрации нового пользователя"""
    response = client.post("/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword",
        "phone_number": "1234567890"
    })
    assert response.status_code == 201, response.json

def test_login(client):
    """Тест входа (логина)"""
    client.post("/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword",
        "phone_number": "1234567890"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200, response.json
    assert "token" in response.json, "JWT-токен отсутствует в ответе"

def test_protected_route_with_token(client):
    """Проверяем доступ с токеном"""
    client.post("/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword",
        "phone_number": "1234567890"
    })
    login_response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword"
    })
    assert login_response.status_code == 200, login_response.json
    token = login_response.json.get("token", None)
    assert token is not None, "JWT-токен отсутствует в ответе"

    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.json

@pytest.fixture
def client():
    """Создаёт тестовый клиент Flask"""
    with app.test_client() as client:
        yield client