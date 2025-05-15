from abc import ABC, abstractmethod

class AuthService(ABC):
    @abstractmethod
    def generate_token(self, user_id: str, email: str) -> str:
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

    @abstractmethod
    def refresh_token(self, token: str) -> str:
        """Refreshes an expired token, returning a new one."""
        pass