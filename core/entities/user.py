from sqlalchemy import Column, String, DateTime
from infrastructure.db.base import Base
from domain.models.user import User
from datetime import datetime
from uuid import UUID, uuid4

class UserModel(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_entity(self) -> User:
        return User(
            user_id=UUID(self.user_id),  # Parse the string as a UUID
            name=self.name,
            email=self.email,
            password_hash=self.password_hash,
            phone_number=self.phone_number,
            role=self.role,
            created_at=self.created_at,
            updated_at=self.updated_at
            )