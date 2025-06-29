from typing import Dict, Any
from domain.models.user_query import UserQuery
from google.genai import types
import google.generativeai as genai
import logging
import os

logger = logging.getLogger(__name__)

# Load system instructions from instruction.txt
INSTRUCTION_FILE = "/domain/services/ai_service/instruction.txt"
if os.path.exists(INSTRUCTION_FILE):
    with open(INSTRUCTION_FILE, "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
else:
    logger.warning("instruction.txt not found, using default system prompt.")
    SYSTEM_PROMPT = "You are a knowledgeable travel guide specialized in Kazakhstan."

class GeminiQueryService:
    def __init__(self, gemini_client):
        self.gemini_client = gemini_client

    def parse_user_query(self, user_text: str) -> UserQuery:
        """
        Use Gemini to extract structured intent from user text.
        Returns a UserQuery domain model.
        """
        prompt = (
            "Extract the main intent, place type (e.g. cafe, restaurant), and any filters (e.g. rating, price) "
            "from this user query. Respond in JSON like: "
            '{"category": "...", "filters": {"rating_min": 4.5, ...}}. '
            f'User query: "{user_text}"'
        )
        gemini_response = self.gemini_client.ask(prompt)
        # Assume gemini_response is a dict with 'category' and 'filters'
        category = gemini_response.get("category")
        filters = gemini_response.get("filters", {})
        return UserQuery(raw_text=user_text, category=category, filters=filters)
    
    def process_query(self, user_text: str):
        import json
        import re

        prompt = (
            f"{SYSTEM_PROMPT}\n"
            f"User query: {user_text}\n"
            "Return a JSON array of locations with name, lat, lon. Example:\n"
            '[{"name": "Astana", "lat": 51.1294, "lon": 71.4491}, ...]'
        )

        try:
            # For google-generativeai, use the GenerativeModel API
            model = self.gemini_client.GenerativeModel(
                model_name="gemini-2.5-flash"
            )
            response = model.generate_content(prompt)
            # The response text is in response.text or response.candidates[0].content.parts[0].text
            text = getattr(response, "text", None)
            if not text and hasattr(response, "candidates"):
                text = response.candidates[0].content.parts[0].text

            # Extract JSON array from the response
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                locations = json.loads(match.group(0))
                return locations
        except Exception as e:
            logger.error(f"Failed to parse Gemini response: {e}")
        return []