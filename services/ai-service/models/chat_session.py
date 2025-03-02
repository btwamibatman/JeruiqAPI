import redis
import json
import os
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis connection
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history = self._load_history()
        self.model = self._initialize_model()
        self.chat = self.model.start_chat(history=self.history)

    def _load_history(self):
        try:
            data = redis_client.get(f"chat_history:{self.session_id}")
            return json.loads(data) if data else []
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []

    def _save_history(self):
        try:
            redis_client.set(f"chat_history:{self.session_id}", json.dumps(self.history), ex=86400)
        except Exception as e:
            logger.error(f"Error saving history: {e}")

    def _initialize_model(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        return genai.GenerativeModel("gemini-2.0-flash")

    def send_message(self, message: str):
        try:
            self.history.append({"role": "user", "parts": [message]})
            response = self.chat.send_message(message)
            self.history.append({"role": "model", "parts": [response.text.strip()]})
            self._save_history()
            return response.text.strip()
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise

    def clear_history(self):
        self.history = []
        redis_client.delete(f"chat_history:{self.session_id}")
        self.chat = self.model.start_chat(history=self.history)

class ChatSessionManager:
    _instances = {}

    @classmethod
    def get_session(cls, session_id: str):
        if session_id not in cls._instances:
            cls._instances[session_id] = ChatSession(session_id)
        return cls._instances[session_id]

    @classmethod
    def clear_session(cls, session_id: str):
        if session_id in cls._instances:
            cls._instances[session_id].clear_history()
            del cls._instances[session_id]

def get_response(user_message: str, session_id: str):
    session = ChatSessionManager.get_session(session_id)
    return session.send_message(user_message)
