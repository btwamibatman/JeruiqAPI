from infrastructure.db.repositories.user_repository import UserRepository
from application.services.password_hasher import PasswordHasher
from application.services.jwt_service import JWTService
from domain.models.user import User as DomainUser
from domain.exceptions import DomainException # Import domain exception
import datetime

class InvalidCredentialsException(DomainException):
    """Custom exception for login failure due to invalid credentials."""
    pass

def login_user(
    email: str,
    plain_password: str,
    user_repository: UserRepository,
    password_hasher: PasswordHasher,
    jwt_service: JWTService
) -> str: # Returns the JWT token string
    """
    Use case to log in a user and generate a JWT token.
    """
    # 1. Find the user by email using the repository
    user = user_repository.get_by_email(email)

    if not user:
        raise InvalidCredentialsException("Invalid email or password.")

    # 2. Verify the password using the password hasher
    if not password_hasher.verify_password(plain_password, user.password_hash):
        raise InvalidCredentialsException("Invalid email or password.")

    # 3. Generate a JWT token using the JWT service
    token = jwt_service.generate_token(user_id=user.user_id)

    # 4. Return the token
    return token