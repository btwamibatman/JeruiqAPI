# domain/services/chat_service/chat_service.py
from domain.models.chat import Chat
from domain.services.ai_service.gemini_ai_model import ChatSession
from uuid import UUID, uuid4

class ChatService:
    def __init__(self):
        self.chat_sessions = {}  # In-memory store; replace with Redis in production

    def start_chat(self, user_id: UUID) -> Chat:
        chat = Chat(session_id=uuid4(), user_id=user_id)
        chat_session = ChatSession(str(chat.session_id))
        self.chat_sessions[str(chat.session_id)] = chat_session
        return chat

    def send_message(self, chat: Chat, message: str) -> str:
        chat.add_message("user", message)
        chat_session = self.chat_sessions.get(str(chat.session_id))
        if not chat_session:
            raise ValueError("Chat session not found")
        response = chat_session.send_message(message)
        chat.add_message("ai", response)
        return response