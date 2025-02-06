from core.ports.auth_service import AuthService
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.auth.password_hasher import PasswordHasher

class UserLogin:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.auth_service: AuthService = JWTAuthService()

    def login(self, email: str, password: str):
        """Аутентификация пользователя и выдача JWT токена"""
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Пользователь не найден")

        if not PasswordHasher.verify_password(password, user.password_hash):
            raise ValueError("Неверный пароль")

        # Генерация JWT-токена
        token = self.auth_service.generate_token(user.user_id, user.email)
        return token
