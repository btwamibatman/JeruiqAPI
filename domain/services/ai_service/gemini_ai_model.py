import google.generativeai as genai
import os
import yaml
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ChatSession:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.config = self._load_config()
        self.instructions = self._load_instructions()
        self._initialize_model()

    def _load_config(self) -> dict:
        """Load configuration from config.yaml."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
            with open(config_path, "r") as config_file:
                config = yaml.safe_load(config_file)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except FileNotFoundError:
            logger.error("config.yaml not found")
            raise FileNotFoundError("config.yaml not found in services/ai_service/")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config.yaml: {str(e)}")
            raise

    def _load_instructions(self) -> dict:
        """Load instructions from instructions.yaml and insert current date/time."""
        try:
            instructions_path = os.path.join(os.path.dirname(__file__), "instructions.yaml")
            with open(instructions_path, "r") as instructions_file:
                instructions = yaml.safe_load(instructions_file)
            logger.info(f"Loaded instructions from {instructions_path}")
            # Insert current date and time into system_prompt
            if "system_prompt" in instructions:
                current_time = datetime.now().strftime("%I:%M %p %z on %A, %B %d, %Y")
                instructions["system_prompt"] = instructions["system_prompt"].replace(
                    "05:08 PM +05 on Wednesday, May 14, 2025", current_time
                )
            return instructions
        except FileNotFoundError:
            logger.warning("instructions.yaml not found, using empty instructions")
            return {"system_prompt": ""}
        except yaml.YAMLError as e:
            logger.error(f"Error parsing instructions.yaml: {str(e)}")
            raise

    def _initialize_model(self):
        """Initialize the Gemini model using config.yaml and instructions.yaml settings."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.error("GEMINI_API_KEY environment variable is not set")
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        try:
            genai.configure(api_key=api_key)

            # Use configuration from config.yaml
            model_name = self.config.get("model_name", "gemini-pro")
            generation_config = self.config.get("generation_config", {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048
            })
            safety_settings = self.config.get("safety_settings", [])

            self.model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            # Use system prompt from instructions.yaml
            system_prompt = self.instructions.get("system_prompt", "")
            initial_messages = []
            self.chat = self.model.start_chat(history=initial_messages)
            if system_prompt:
                self.chat.send_message(system_prompt)

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
            return response.text

        except Exception as e:
            logger.error(f"Error in send_message: {str(e)}")
            raise