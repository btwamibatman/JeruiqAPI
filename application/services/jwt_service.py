import jwt
import datetime
from typing import Optional

class JWTService:
    """Handles JWT token generation and verification."""

    # Modify __init__ to accept expiration_minutes
    def __init__(self, secret_key: str, expiration_minutes: int, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.expiration_minutes = expiration_minutes # Store expiration as an instance attribute
        self.algorithm = algorithm

    def generate_token(self, user_id: str, expires_delta: datetime.timedelta = None) -> str:
        """Generates a JWT token for a user ID."""
        if expires_delta is None:
            # Use the instance attribute for expiration
            expires_delta = datetime.timedelta(minutes=self.expiration_minutes)

        # Use UTC timezone for consistency
        expire = datetime.datetime.now(datetime.UTC) + expires_delta
        # 'sub' (subject) is standard claim for user ID
        to_encode = {"exp": expire, "sub": str(user_id)}
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verifies a JWT token and returns the user ID if valid."""
        try:
            # Ensure algorithms is a list
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except jwt.ExpiredSignatureError:
            # Token has expired
            print("JWT verification failed: Token has expired.") # Optional: add logging
            return None
        except jwt.InvalidTokenError:
            # Token is invalid (e.g., wrong signature, wrong algorithm)
            print("JWT verification failed: Invalid token.") # Optional: add logging
            return None
        except Exception as e:
            # Catch any other unexpected errors during decode
            print(f"JWT verification failed with unexpected error: {e}") # Optional: add logging
            return None