import pytest
from unittest.mock import MagicMock
from domain.services.user_service.user_service import UserService  # Adjust import
from domain.models.user import User

@pytest.fixture
def user_service():
    repo = MagicMock()
    return UserService(repository=repo)

def test_create_user(user_service):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password"
    }
    user_service.repository.create.return_value = User(id=1, **user_data)
    
    user = user_service.create_user(**user_data)
    
    assert user.id == 1
    assert user.username == "testuser"
    user_service.repository.create.assert_called()

def test_create_user_invalid_email(user_service):
    with pytest.raises(ValueError):
        user_service.create_user(
            username="testuser",
            email="invalid",
            password="password"
        )