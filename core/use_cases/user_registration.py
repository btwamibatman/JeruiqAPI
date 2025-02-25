from core.ports.auth_service import AuthService
from core.ports.user_repository import UserRepository
from adapters.auth.password_hasher import PasswordHasher
from core.entities.user import User

class UserRegistration:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service
    def register_user(self, name: str, email: str, password: str, phone_number: str):
        """Регистрирует нового пользователя"""
        if self.user_repository.get_by_email(email):
            raise ValueError("Пользователь с таким email уже существует")
        print(password)
        hashed_password = PasswordHasher.hash_password(password)
        print(f"Generated Hash: {hashed_password}") 

        user = User(
            name=name,
            email=email,
            password_hash=hashed_password,  # Сохраняем хеш
            phone_number=phone_number
        )
        self.user_repository.save(user)
        return user