from core.ports.user_repository import UserRepository
from core.ports.auth_service import AuthService
from domain.services.user_service.user_service import UserService
from domain.models.user import User

class UserRegistration:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def register_user(self, name: str, email: str, password: str, phone_number: str) -> User:
        hashed_password = self.auth_service.hash_password(password)
        user = UserService.create_user(
            name=name,
            email=email,
            password=hashed_password,  # Pass the hashed password
            phone_number=phone_number
        )
        self.user_repository.save(user)
        return user