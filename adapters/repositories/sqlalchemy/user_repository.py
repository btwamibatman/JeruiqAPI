from core.entities.user import User, UserModel
from infrastructure.db import SessionLocal

class SQLAlchemyUserRepository:
    """Репозиторий пользователей через SQLAlchemy"""

    def __init__(self):
        self.session = SessionLocal()

    def get_by_id(self, user_id: str) -> User:
        user_model = self.session.query(UserModel).filter_by(user_id=user_id).first()
        return user_model.to_entity() if user_model else None

    def get_by_email(self, email: str) -> User:
        user_model = self.session.query(UserModel).filter_by(email=email).first()
        return user_model.to_entity() if user_model else None

    def save(self, user: User) -> None:
        """Сохраняем пользователя в БД"""
        user_model = UserModel(
            user_id=user.user_id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            phone_number=user.phone_number,
            role=user.role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.session.add(user_model)
        self.session.commit()
