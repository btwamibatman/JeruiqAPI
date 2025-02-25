from abc import ABC, abstractmethod
from core.entities.user import User

class UserRepository(ABC):
    """Абстрактный интерфейс для работы с пользователями"""

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def save(self, user: User) -> None:
        pass
