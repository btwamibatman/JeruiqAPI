from typing import Dict, Any
from domain.models.user_query import UserQuery

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