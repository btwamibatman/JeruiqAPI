import unittest
from core.use_cases.user_registration import UserRegistration
from core.use_cases.user_login import UserLogin
from core.entities.user import User
from core.ports.user_repository import UserRepository
from adapters.auth.password_hasher import PasswordHasher
from adapters.auth.jwt_auth import JWTAuthService

class MockUserRepository(UserRepository):
    """Фейковый репозиторий для тестов"""
    def __init__(self):
        self.users = {}
    
    def create_user(self, user):
        self.users[user.user.email] = user

    def get_by_email(self, email: str):
        return next((u for u in self.users.values() if u.email == email), None)

    def save(self, user: User):
        self.users[user.user_id] = user
    
    def delete(self, user_id: str):
        del self.users[user_id]

    def get_all_users(self):
        return list(self.users.values())

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.user_repo = MockUserRepository()
        self.user_registration = UserRegistration(self.user_repo)
        self.user_login = UserLogin(self.user_repo)
        self.auth_service = JWTAuthService()

    def test_user_registration(self):
        user = self.user_registration.register_user(
            name="Test User",
            email="test@example.com",
            password="securepassword",
            phone_number="1234567890"
        )
        self.assertEqual(user.email, "test@example.com")

    def test_user_login(self):
        """Проверяем вход в систему"""
        self.user_registration.register_user(
            name="Test User",
            email="test@example.com",
            password="securepassword",
            phone_number="1234567890"
        )
        token = self.user_login.login(email="test@example.com", password="securepassword")
        self.assertTrue(token)

    def test_invalid_login(self):
        """Логин с неверным паролем"""
        self.user_registration.register_user(
            name="Test User",
            email="test@example.com",
            password="securepassword",
            phone_number="1234567890"
        )
        with self.assertRaises(ValueError):
            self.user_login.login(email="test@example.com", password="wrongpassword")

    def test_jwt_verification(self):
        """Проверяем валидность токена"""
        token = self.auth_service.generate_token("123", "test@example.com")
        decoded = self.auth_service.verify_token(token)
        self.assertEqual(decoded["email"], "test@example.com")

if __name__ == "__main__":
    unittest.main()
