import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from core.ports.auth_service import AuthService

class JWTAuthService(AuthService):
    SECRET_KEY = "your_secret_key"

    def generate_token(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.timedelta(hours=12),
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def hash_password(self, password: str) -> str:
        return generate_password_hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return check_password_hash(hashed_password, password)
# Compare this snippet from core/ports/auth_service.py: