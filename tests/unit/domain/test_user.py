import pytest
from domain.models.user import User
from uuid import uuid4

def test_user_creation():
    user = User(
        user_id=uuid4(),
        name="John Doe",
        email="john@example.com",
        password_hash="hashedpassword",
        phone_number="1234567890",
        role="user"
    )
    assert user.email == "john@example.com"
    assert user.role == "user"

def test_user_invalid_email():
    with pytest.raises(ValueError):
        User(user_id=uuid4(), name="John", email="invalid", password_hash="hash", phone_number="12345", role="user")

def test_user_invalid_phone_number():
    with pytest.raises(ValueError):
        User(user_id=uuid4(), name="John", email="john@example.com", password_hash="hash", phone_number="123", role="user")