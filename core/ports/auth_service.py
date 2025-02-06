from abc import ABC, abstractmethod

class AuthService(ABC):
    """Abstract Authentication Service Interface"""

    @abstractmethod
    def generate_token(self, user_id: str) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass
# Compare this snippet from adapters/auth/jwt_auth.py: