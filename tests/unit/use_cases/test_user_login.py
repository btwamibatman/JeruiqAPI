import pytest
from unittest.mock import MagicMock
from core.use_cases.user_login import UserLogin  # Adjust import
from domain.models.user import User

@pytest.fixture
def user_login():
    repo = MagicMock()
    auth_service = MagicMock()
    return UserLogin(repository=repo, auth_service=auth_service)

def test_user_login_success(user_login):
    user = User(id=1, username="testuser", email="test@example.com", password_hash="hashed")
    user_login.repository.get_by_username.return_value = user
    user_login.auth_service.verify_password.return_value = True
    user_login.auth_service.generate_token.return_value = "jwt_token"
    
    token = user_login.execute(username="testuser", password="password")
    
    assert token == "jwt_token"
    user_login.repository.get_by_username.assert_called_with("testuser")
    user_login.auth_service.verify_password.assert_called_with("password", "hashed")

def test_user_login_invalid_password(user_login):
    user = User(id=1, username="testuser", email="test@example.com", password_hash="hashed")
    user_login.repository.get_by_username.return_value = user
    user_login.auth_service.verify_password.return_value = False
    
    with pytest.raises(ValueError):
        user_login.execute(username="testuser", password="wrong")