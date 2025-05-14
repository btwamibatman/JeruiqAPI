from core.entities.user import UserModel
from domain.models.user import User
from infrastructure.db import SessionLocal
from uuid import UUID

class SQLAlchemyUserRepository:
    """Репозиторий пользователей через SQLAlchemy"""

    def __init__(self):
        self.session = SessionLocal()

    def get_by_email(self, email: str) -> User:
        """Получение пользователя по email"""
        user_model = self.session.query(UserModel).filter_by(email=email).first()
        if user_model:
            print(f"User found: {user_model.email}, Password Hash: {user_model.password_hash}")  # Лог для отладки
        return user_model.to_entity() if user_model else None

    def get_by_id(self, user_id: str) -> User:
        """Получение пользователя по ID"""
        user_model = self.session.query(UserModel).filter_by(user_id=user_id).first()
        return user_model.to_entity() if user_model else None

    def save(self, user: User) -> None:
        """Сохранение пользователя в БД"""
        user_model = UserModel(
            user_id=str(user.user_id),
            name=user.name,  # Added
            email=user.email,
            password_hash=user.password_hash,
            phone_number=user.phone_number,  # Added
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(user_model)
        self.session.commit()