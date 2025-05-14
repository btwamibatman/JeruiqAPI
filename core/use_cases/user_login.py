from core.ports.user_repository import UserRepository
from core.ports.auth_service import AuthService
from domain.services.user_service.user_service import UserService
from domain.models.user import User

class UserLogin:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    def login_user(self, email: str, password: str) -> str:
        user = self.user_repository.get_by_email(email)
        if not user or not UserService.verify_password(user, password):
            raise ValueError("Invalid email or password")
        return self.auth_service.generate_token(user.user_id, user.email)