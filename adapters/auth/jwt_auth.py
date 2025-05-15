import jwt
import datetime
from core.ports.auth_service import AuthService
from adapters.auth.password_hasher import PasswordHasher
from infrastructure.config import ActiveConfig
from flask import request, jsonify, current_app
from functools import wraps
from domain.models.user import User

class JWTAuthService(AuthService):
    def __init__(self, password_hasher: PasswordHasher = None):
        self.password_hasher = password_hasher or PasswordHasher()
        self.secret_key = ActiveConfig.SECRET_KEY  # Use secret key from config

    def generate_token(self, user_id: str, email: str) -> str:
        payload = {
            "user_id": str(user_id),
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
            "iat": datetime.datetime.utcnow()  # Added for better token validation
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def refresh_token(self, old_token: str) -> str:
        payload = self.verify_token(old_token)
        return self.generate_token(payload["user_id"], payload["email"])

    def hash_password(self, password: str) -> str:
        return self.password_hasher.hash_password(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.password_hasher.verify_password(password, hashed_password)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            payload = JWTAuthService().verify_token(token)
            # Attach user info to request context for use in routes
            current_app.config['current_user'] = User(
                user_id=payload['user_id'],
                name='',  # Placeholder; fetch from DB if needed
                email=payload['email'],
                password_hash='',  # Not needed here
                phone_number=None,
                role='user'  # Default or fetch from DB
            )
        except ValueError as e:
            return jsonify({'error': str(e)}), 401
        return f(current_app.config['current_user'], *args, **kwargs)
    return decorated