import pytest
from unittest.mock import MagicMock
from google.api_core.exceptions import GoogleAPIError
from adapters.error_handlers.ai_error_handlers import AIErrorHandler
import logging

@pytest.fixture
def ai_error_handler():
    return AIErrorHandler()

def test_handle_rate_limit_error(ai_error_handler, caplog):
    caplog.set_level(logging.ERROR)
    error = GoogleAPIError("Rate limit exceeded")
    
    result = ai_error_handler.handle_google_api_error(error)
    
    assert result == {"error": "Rate limit exceeded", "status": 429}
    assert "Google API error: Rate limit exceeded" in caplog.text

def test_handle_generic_api_error(ai_error_handler, caplog):
    caplog.set_level(logging.ERROR)
    error = GoogleAPIError("Unknown error")
    
    result = ai_error_handler.handle_google_api_error(error)
    
    assert result == {"error": "AI service error", "status": 500}
    assert "Google API error: Unknown error" in caplog.text