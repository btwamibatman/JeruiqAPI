from sqlalchemy import Column, String, DateTime, ForeignKey
from infrastructure.db.base import Base
from datetime import datetime
from uuid import uuid4

class ChatModel(Base):
    __tablename__ = "chats"

    chat_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)