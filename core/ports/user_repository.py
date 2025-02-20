from abc import ABC, abstractmethod
from core.entities.user import User

class UserRepository(ABC):
    """Interface defining user repository operations."""

    @abstractmethod
    def save(self, user: User) -> None:
        """Saves a new user to the database."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        """Retrieves a user by email."""
        pass

    @abstractmethod
    def get_all_users(self) -> list[User]:
        """Retrieves all users."""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> None:
        """Deletes a user by ID."""
        pass
