from flask import session
import google.generativeai as genai
import os
from typing import Dict, List, Optional

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, List[str]]] = []
        self.model = self._initialize_model()
        self.chat = self.model.start_chat(history=self.history)
    
    @staticmethod
    def _initialize_model():
        """Initialize the Gemini model with configuration."""
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }
        
        return genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config
        )
    
    def send_message(self, message: str) -> str:
        """Send a message and get response from the model."""
        if not message.strip():
            raise ValueError("Message cannot be empty")
        
        # Add user message to history
        self.history.append({"role": "user", "parts": [message]})
        
        # Get response from model
        response = self.chat.send_message(message)
        model_response = response.text.strip()
        
        # Add model response to history
        self.history.append({"role": "model", "parts": [model_response]})
        
        return model_response
    
    def clear_history(self):
        """Clear the conversation history."""
        self.history = []
        self.chat = self.model.start_chat(history=self.history)

class ChatSessionManager:
    _instances: Dict[str, ChatSession] = {}
    
    @classmethod
    def get_session(cls, session_id: str) -> ChatSession:
        """Get or create a chat session for the given session ID."""
        if session_id not in cls._instances:
            cls._instances[session_id] = ChatSession(session_id)
        return cls._instances[session_id]
    
    @classmethod
    def clear_session(cls, session_id: str):
        """Clear a specific chat session."""
        if session_id in cls._instances:
            del cls._instances[session_id]
    
    @classmethod
    def clear_all_sessions(cls):
        """Clear all chat sessions."""
        cls._instances.clear()

def get_response(user_message: str, session_id: Optional[str] = None) -> str:
    """
    Get a response from Gemini AI based on the user's input.
    
    Args:
        user_message: The message from the user
        session_id: Optional session identifier for maintaining conversation context
    
    Returns:
        The model's response
    
    Raises:
        ValueError: If the message is empty or session management fails
        Exception: For other errors during processing
    """
    if not session_id:
        session_id = session.get('user_id')  # Get from Flask session
        if not session_id:
            raise ValueError("No session ID provided")
    
    try:
        chat_session = ChatSessionManager.get_session(session_id)
        return chat_session.send_message(user_message)
    except Exception as e:
        # Log the error here if you have logging configured
        raise Exception(f"Failed to get response: {str(e)}")