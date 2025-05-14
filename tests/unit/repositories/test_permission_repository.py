import pytest
from unittest.mock import MagicMock
from adapters.repositories.sqlalchemy.permission_repository import PermissionRepository  # Adjust import
from domain.models.permission import Permission
from sqlalchemy.orm import Session

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_create_permission(mock_session):
    repo = PermissionRepository(mock_session)
    permission = Permission(id=1, name="read:chat", description="Read chat")
    
    repo.create(permission)
    
    mock_session.add.assert_called_with(permission)
    mock_session.commit.assert_called_once()

def test_get_by_id(mock_session):
    repo = PermissionRepository(mock_session)
    permission = Permission(id=1, name="read:chat", description="Read chat")
    mock_session.query.return_value.filter.return_value.first.return_value = permission
    
    result = repo.get_by_id(1)
    
    assert result == permission
    mock_session.query.assert_called_with(Permission)