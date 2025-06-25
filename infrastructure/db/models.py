from sqlalchemy import Column, String, Integer, Float, Boolean
from infrastructure.db.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="user", nullable=False)

    def __repr__(self):
        return f"<User(id='{self.user_id}', email='{self.email}')>"