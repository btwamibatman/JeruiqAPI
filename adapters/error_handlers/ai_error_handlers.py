import logging
from google.api_core.exceptions import GoogleAPIError

logger = logging.getLogger(__name__)

class AIErrorHandler:
    @staticmethod
    def handle_google_api_error(error: GoogleAPIError):
        logger.error(f"Google API error: {str(error)}")
        if "rate limit" in str(error).lower():
            return {"error": "Rate limit exceeded", "status": 429}
        return {"error": "AI service error", "status": 500}