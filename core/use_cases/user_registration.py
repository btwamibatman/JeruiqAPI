from core.entities.user import User
from core.ports.user_repository import UserRepository
from core.ports.auth_service import AuthService
from adapters.auth.jwt_auth import JWTAuthService

class UserRegistration:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def register_user(self, name, email, password, phone_number):
        """Регистрирует нового пользователя"""
        hashed_password = self.auth_service.hash_password(password)
        new_user = User(
            user_id=None,  # UUID сгенерируется автоматически
            name=name,
            email=email,
            password_hash=hashed_password,
            phone_number=phone_number
        )

        self.user_repository.save(new_user)
        return new_user
