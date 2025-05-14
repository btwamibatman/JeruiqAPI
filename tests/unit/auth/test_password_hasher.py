import pytest
import bcrypt
from adapters.auth.password_hasher import PasswordHasher  # Adjust import

@pytest.fixture
def password_hasher():
    return PasswordHasher()

def test_hash_password(password_hasher):
    password = "testpassword"
    hashed = password_hasher.hash_password(password)
    assert bcrypt.checkpw(password.encode(), hashed)

def test_verify_password(password_hasher):
    password = "testpassword"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    assert password_hasher.verify_password(password, hashed)
    assert not password_hasher.verify_password("wrongpassword", hashed)