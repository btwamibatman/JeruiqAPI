import pytest
from unittest.mock import MagicMock
from adapters.repositories.sqlalchemy.role_repository import RoleRepository  # Adjust import
from domain.models.role import Role
from sqlalchemy.orm import Session

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_create_role(mock_session):
    repo = RoleRepository(mock_session)
    role = Role(id=1, name="admin", description="Admin role")
    
    repo.create(role)
    
    mock_session.add.assert_called_with(role)
    mock_session.commit.assert_called_once()

def test_get_by_id(mock_session):
    repo = RoleRepository(mock_session)
    role = Role(id=1, name="admin", description="Admin role")
    mock_session.query.return_value.filter.return_value.first.return_value = role
    
    result = repo.get_by_id(1)
    
    assert result == role
    mock_session.query.assert_called_with(Role)