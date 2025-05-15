from abc import ABC, abstractmethod
from domain.models.user import User

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass