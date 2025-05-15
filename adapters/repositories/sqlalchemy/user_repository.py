from core.entities.user import UserModel
from domain.models.user import User
from infrastructure.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

class SQLAlchemyUserRepository:
    """Репозиторий пользователей через SQLAlchemy"""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def get_by_email(self, email: str) -> User:
        """Получение пользователя по email"""
        with self.session_factory() as session:
            user_model = session.query(UserModel).filter_by(email=email).first()
            if user_model:
                logger.debug(f"User found: {user_model.email}, Password Hash: {user_model.password_hash}")
            return user_model.to_entity() if user_model else None

    def get_by_id(self, user_id: str) -> User:
        """Получение пользователя по ID"""
        with self.session_factory() as session:
            user_model = session.query(UserModel).filter_by(user_id=user_id).first()
            return user_model.to_entity() if user_model else None

    def save(self, user: User) -> None:
        """Сохранение пользователя в БД"""
        try:
            user_model = UserModel(
                user_id=str(user.user_id),
                name=user.name,
                email=user.email,
                password_hash=user.password_hash,
                phone_number=user.phone_number,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            with self.session_factory() as session:
                session.add(user_model)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error while saving user: {str(e)}")
            raise