from core.entities.chat import ChatModel  # Adjust import based on your structure
from domain.models.chat import Chat
from infrastructure.db import SessionLocal

class SQLAlchemyChatRepository:
    """Репозиторий чатов через SQLAlchemy"""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def create(self, chat: Chat) -> Chat:
        """Создание записи чата в БД"""
        chat_model = ChatModel(
            id=chat.id,
            user_id=chat.user_id,
            message=chat.message,
            response=chat.response,
            timestamp=chat.timestamp
        )
        with self.session_factory() as session:
            session.add(chat_model)
            session.commit()
        return chat

    def get_by_id(self, chat_id: int) -> Chat:
        """Получение чата по ID"""
        with self.session_factory() as session:
            chat_model = session.query(ChatModel).filter_by(id=chat_id).first()
            return chat_model.to_entity() if chat_model else None