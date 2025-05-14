import pytest
from unittest.mock import MagicMock
from domain.services.ai_service.chat_service import ChatService  # Adjust import

@pytest.fixture
def chat_service(mock_gemini_client):
    gemini_model = MagicMock()
    gemini_model.generate.return_value = "AI response"
    return ChatService(gemini_model=gemini_model)

def test_process_message(chat_service):
    result = chat_service.process_message(user_id=1, message="Hello")
    assert result == {"response": "AI response", "user_id": 1}
    chat_service.gemini_model.generate.assert_called_with("Hello")

def test_process_empty_message(chat_service):
    with pytest.raises(ValueError):
        chat_service.process_message(user_id=1, message="")