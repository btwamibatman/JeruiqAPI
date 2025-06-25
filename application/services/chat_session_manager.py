from uuid import uuid4 as uuid
# Assuming ChatSession is defined elsewhere, e.g., in domain/services/ai_service/
from domain.services.ai_service.gemini_ai_model import ChatSession # Adjust import path if needed

class ChatSessionManager:
    def __init__(self):
        self.chat_sessions = {} # Manages sessions state

    def get_session(self, session_id: str = None) -> ChatSession:
        """Gets an existing session or creates a new one."""
        if session_id is None or session_id not in self.chat_sessions:
            new_session_id = str(uuid())
            self.chat_sessions[new_session_id] = ChatSession(new_session_id)
            return self.chat_sessions[new_session_id]
        return self.chat_sessions[session_id]

    def get_session_id(self, session: ChatSession) -> str:
        """Gets the ID for a given session object."""
        # This is a simple lookup; more complex logic might be needed
        for session_id, s in self.chat_sessions.items():
            if s is session:
                return session_id
        return None # Should not happen if session was obtained via get_session