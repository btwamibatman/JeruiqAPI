import pytest
from domain.models.role import Role  # Adjust import

@pytest.fixture
def role_data():
    return {
        "id": 1,
        "name": "admin",
        "description": "Administrator role"
    }

def test_role_creation(role_data):
    role = Role(**role_data)
    assert role.id == 1
    assert role.name == "admin"
    assert role.description == "Administrator role"

def test_role_invalid_name():
    invalid_data = {
        "id": 2,
        "name": "",
        "description": "Invalid role"
    }
    with pytest.raises(ValueError):
        Role(**invalid_data)