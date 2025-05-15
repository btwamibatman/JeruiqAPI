from domain.models.user import User
from adapters.auth.password_hasher import PasswordHasher  # Adjust path if needed
from uuid import uuid4
from datetime import datetime
from adapters.auth.jwt_auth import JWTAuthService  # Adjust path if needed

# domain/services/user_service/user_service.py
class UserService:
    @staticmethod
    def create_user(email: str, password: str, name: str, phone_number: str, repo=None):
        hashed_password = JWTAuthService().hash_password(password)
        user = User(
            user_id=uuid4(),  # Pass UUID object directly
            email=email,
            password_hash=hashed_password,
            name=name,
            phone_number=phone_number,
            role="user",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        if repo:
            repo.save(user)
        return user
    
    @staticmethod
    def login_user(email: str, password: str, repo, auth_service=None):
        if auth_service is None:
            auth_service = JWTAuthService()
        user = repo.get_by_email(email)  # Assume repo is injected
        if not user or not auth_service.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        token = auth_service.generate_token(user.user_id, user.email)
        return token

    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        """Verify a user's password."""
        return PasswordHasher.verify_password(password, user.password_hash)