from domain.models.chat import Chat
from domain.services.ai_service.gemini_ai_model import ChatSession  # Adjust path based on your structure
from uuid import UUID, uuid4

class ChatService:
    @staticmethod
    def start_chat(user_id: UUID) -> Chat:
        """Start a new chat session for a user."""
        chat = Chat(session_id=uuid4(), user_id=user_id)
        # Initialize Gemini ChatSession (simplified; adjust based on your needs)
        chat_session = ChatSession(str(chat.session_id))
        return chat

    @staticmethod
    def send_message(chat: Chat, message: str) -> str:
        """Send a message to the chat and get an AI response."""
        chat.add_message("user", message)
        # Use Gemini AI to generate a response
        chat_session = ChatSession(str(chat.session_id))
        response = chat_session.send_message(message)
        chat.add_message("ai", response)
        return response