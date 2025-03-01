from core.ports.auth_service import AuthService
from core.ports.user_repository import UserRepository
from adapters.auth.password_hasher import PasswordHasher
from adapters.auth.jwt_auth import JWTAuthService

class UserLogin:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.jwt_service = JWTAuthService()

    def login(self, email: str, password: str):
        """Аутентификация пользователя и выдача JWT-токена"""
        user = self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Пользователь не найден")
        print(user.email)
        print(f"Stored hash: {user.password_hash}")
        print(f"Checking password for {user.email}: {password} vs {user.password_hash}")
        print(f"Password matches: {PasswordHasher.verify_password(password, user.password_hash)}")  

        # Проверяем пароль
        if not PasswordHasher.verify_password(password, user.password_hash):
            raise ValueError("Неверный email или пароль")

        # Генерация JWT-токена
        token = self.jwt_service.generate_token(user.user_id, user.email)
        return token
