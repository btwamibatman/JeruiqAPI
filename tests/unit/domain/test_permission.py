import pytest
from domain.models.permission import Permission  # Adjust import

@pytest.fixture
def permission_data():
    return {
        "id": 1,
        "name": "read:chat",
        "description": "Read chat messages"
    }

def test_permission_creation(permission_data):
    permission = Permission(**permission_data)
    assert permission.id == 1
    assert permission.name == "read:chat"
    assert permission.description == "Read chat messages"

def test_permission_invalid_name():
    invalid_data = {
        "id": 2,
        "name": "",
        "description": "Invalid permission"
    }
    with pytest.raises(ValueError):
        Permission(**invalid_data)