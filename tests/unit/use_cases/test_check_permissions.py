import pytest
from unittest.mock import MagicMock
from core.use_cases.check_permissions import CheckPermissions  # Adjust import

@pytest.fixture
def check_permissions():
    repo = MagicMock()
    return CheckPermissions(repository=repo)

def test_check_permissions_granted(check_permissions):
    check_permissions.repository.has_permission.return_value = True
    result = check_permissions.execute(user_id=1, permission="read:chat")
    assert result is True
    check_permissions.repository.has_permission.assert_called_with(user_id=1, permission="read:chat")

def test_check_permissions_denied(check_permissions):
    check_permissions.repository.has_permission.return_value = False
    result = check_permissions.execute(user_id=1, permission="write:chat")
    assert result is False