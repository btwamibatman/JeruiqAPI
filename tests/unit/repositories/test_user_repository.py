import pytest
from unittest.mock import MagicMock
from adapters.repositories.sqlalchemy.user_repository import UserRepository  # Adjust import
from domain.models.user import User
from sqlalchemy.orm import Session

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_create_user(mock_session):
    repo = UserRepository(mock_session)
    user = User(id=1, username="testuser", email="test@example.com")
    
    repo.create(user)
    
    mock_session.add.assert_called_with(user)
    mock_session.commit.assert_called_once()

def test_get_by_id(mock_session):
    repo = UserRepository(mock_session)
    user = User(id=1, username="testuser", email="test@example.com")
    mock_session.query.return_value.filter.return_value.first.return_value = user
    
    result = repo.get_by_id(1)
    
    assert result == user
    mock_session.query.assert_called_with(User)