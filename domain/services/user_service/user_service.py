from domain.models.user import User
from adapters.auth.password_hasher import PasswordHasher  # Adjust path if needed
from uuid import uuid4

class UserService:
    @staticmethod
    def create_user(email: str, password: str, name: str, phone_number: str, role: str = "user") -> User:
        """Create a new user with hashed password."""
        password_hash = PasswordHasher.hash_password(password)
        return User(
            user_id=uuid4(),
            name=name,
            email=email,
            password_hash=password_hash,
            phone_number=phone_number,
            role=role
        )

    @staticmethod
    def verify_password(user: User, password: str) -> bool:
        """Verify a user's password."""
        return PasswordHasher.verify_password(password, user.password_hash)