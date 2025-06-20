from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from infrastructure.db.base import Base

class User:
    """Чистая сущность пользователя (НЕ SQLAlchemy)"""
    def __init__(self, name: str, email: str, password_hash: str, phone_number: str, user_id: str = None, role: str = "user", created_at=None, updated_at=None):
        self.user_id = user_id or str(uuid4())  # Генерация UUID
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.phone_number = phone_number
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self):
        return f"<User {self.name} ({self.email})>"

class UserModel(Base):
    """Модель пользователя для SQLAlchemy"""
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_entity(self) -> User:
        """Конвертирует SQLAlchemy-модель в чистый объект `User`"""
        return User(
            user_id=self.user_id,
            name=self.name,
            email=self.email,
            password_hash=self.password_hash,
            phone_number=self.phone_number,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
