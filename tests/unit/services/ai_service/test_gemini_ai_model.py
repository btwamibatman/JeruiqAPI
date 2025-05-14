import pytest
from unittest.mock import patch
from domain.services.ai_service.gemini_ai_model import GeminiAIModel  # Adjust import

@pytest.fixture
def gemini_model():
    return GeminiAIModel(api_key="test_key")

def test_gemini_generate_response(mock_gemini_client, gemini_model):
    response = gemini_model.generate("Test prompt")
    assert response == "Mocked AI response"
    mock_gemini_client.assert_called_with(model_name="gemini-pro")
    mock_gemini_client.return_value.generate_content.assert_called_with("Test prompt")

def test_gemini_generate_empty_prompt(gemini_model):
    with pytest.raises(ValueError):
        gemini_model.generate("")