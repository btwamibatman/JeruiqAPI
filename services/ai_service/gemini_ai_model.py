import google.generativeai as genai
import os
import redis
import json
from typing import Dict, List
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Redis connection
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))

# Load system instructions from instruction.txt
INSTRUCTION_FILE = "instruction.txt"
if os.path.exists(INSTRUCTION_FILE):
    with open(INSTRUCTION_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
else:
    logger.warning("instruction.txt not found, using default system prompt.")
    SYSTEM_PROMPT = "You are a knowledgeable travel guide specialized in Kazakhstan."

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, str]] = self._load_history()
        self.model = self._initialize_model()
        self.chat = self.model.start_chat(history=self.history)
    
    def _load_history(self) -> List[Dict[str, str]]:
        """Load conversation history from Redis."""
        try:
            history_data = redis_client.get(f"chat_history:{self.session_id}")
            if history_data:
                return json.loads(history_data)
            return []
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return []
    
    def _save_history(self):
        """Save conversation history to Redis."""
        try:
            redis_client.set(
                f"chat_history:{self.session_id}", 
                json.dumps(self.history),
                ex=86400  # Expires in 24 hours
            )
        except Exception as e:
            logger.error(f"Error saving history: {e}")

    @staticmethod
    def _initialize_model():
        """Initialize the Gemini model with system instructions."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        
        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
            "response_mime_type": "text/plain",
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config
        )

        # Start the chat with system instructions
        return model.start_chat(history=[{"role": "system", "parts": [SYSTEM_PROMPT]}])

    def send_message(self, message: str) -> str:
        """Send a message and get a response from the model."""
        if not message.strip():
            raise ValueError("Message cannot be empty")
        
        try:
            # Add user message to history
            self.history.append({"role": "user", "parts": [message]})
            
            # Get response from model
            response = self.chat.send_message(message)
            model_response = response.text.strip()
            
            # Add model response to history
            self.history.append({"role": "model", "parts": [model_response]})
            
            # Save updated history
            self._save_history()
            
            return model_response
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise