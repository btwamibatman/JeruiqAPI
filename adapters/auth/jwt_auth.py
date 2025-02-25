import jwt
import datetime
import bcrypt
from core.ports.auth_service import AuthService

class JWTAuthService(AuthService):
    SECRET_KEY = "TOUrc2ek6vIAVV6TbVkzQiTe"
    
    def generate_token(self, user_id: str, email: str) -> str:
        payload = {
            "user_id": str(user_id),
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
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
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
