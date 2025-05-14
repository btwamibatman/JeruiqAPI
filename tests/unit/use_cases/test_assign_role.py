import pytest
from unittest.mock import MagicMock
from core.use_cases.assign_role import AssignRole  # Adjust import
from domain.models.user import User
from domain.models.role import Role

@pytest.fixture
def assign_role():
    repo = MagicMock()
    return AssignRole(repository=repo)

def test_assign_role(assign_role):
    user = User(id=1, username="testuser", email="test@example.com")
    role = Role(id=1, name="admin")
    
    assign_role.execute(user_id=1, role_id=1)
    
    assign_role.repository.assign_role.assert_called_with(user_id=1, role_id=1)

def test_assign_role_invalid_user(assign_role):
    with pytest.raises(ValueError):
        assign_role.execute(user_id=0, role_id=1)