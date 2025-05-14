import google.generativeai as genai
import os
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the Gemini model."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        try:
            genai.configure(api_key=api_key)

            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]

            self.model = genai.GenerativeModel(
                model_name="gemini-2.0-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            self.chat = self.model.start_chat(history=[])
            logger.info(f"Chat model initialized successfully for session {self.session_id}")

        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise
    
    def send_message(self, message: str) -> str:
        """Send a message and get a response from the model."""
        try:
            if not message.strip():
                raise ValueError("Message cannot be empty")

            logger.debug(f"Sending message to model: {message[:50]}...")
            response = self.chat.send_message(message)

            if not response.text:
                raise ValueError("Empty response from model")
            
            logger.debug(f"Received clean response from model: {response.text[:50]}...")
            return response.text.strip()

        except Exception as e:
            logger.error(f"Error in send_message: {str(e)}")
            raise