import pytest
import jwt
from adapters.auth.jwt_auth import JWTAuth  # Adjust import
from datetime import datetime, timedelta

@pytest.fixture
def jwt_auth():
    return JWTAuth(secret_key="test_secret", algorithm="HS256")

def test_generate_token(jwt_auth):
    user_id = 1
    token = jwt_auth.generate_token(user_id)
    
    decoded = jwt.decode(token, "test_secret", algorithms=["HS256"])
    assert decoded["user_id"] == user_id
    assert "exp" in decoded

def test_validate_token(jwt_auth):
    user_id = 1
    token = jwt_auth.generate_token(user_id)
    validated_user_id = jwt_auth.validate_token(token)
    
    assert validated_user_id == user_id

def test_validate_expired_token(jwt_auth):
    user_id = 1
    expired_token = jwt.encode(
        {"user_id": user_id, "exp": datetime.utcnow() - timedelta(seconds=1)},
        "test_secret",
        algorithm="HS256"
    )
    
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt_auth.validate_token(expired_token)