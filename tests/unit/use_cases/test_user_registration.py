import pytest
from unittest.mock import MagicMock
from core.use_cases.user_registration import UserRegistration  # Adjust import
from domain.models.user import User

@pytest.fixture
def user_registration():
    repo = MagicMock()
    auth_service = MagicMock()
    return UserRegistration(repository=repo, auth_service=auth_service)

def test_user_registration_success(user_registration):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"
    }
    user_registration.auth_service.hash_password.return_value = "hashed"
    user_registration.repository.create.return_value = User(id=1, **user_data, password_hash="hashed")
    
    user = user_registration.execute(**user_data)
    
    assert user.id == 1
    assert user.username == "testuser"
    user_registration.auth_service.hash_password.assert_called_with("password")
    user_registration.repository.create.assert_called()

def test_user_registration_invalid_email(user_registration):
    with pytest.raises(ValueError):
        user_registration.execute(
            username="testuser",
            email="invalid",
            password="password"
        )