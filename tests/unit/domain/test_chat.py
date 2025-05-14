import pytest
from domain.models.chat import Chat  # Adjust import
from datetime import datetime

@pytest.fixture
def chat_data():
    return {
        "id": 1,
        "user_id": 1,
        "message": "Hello",
        "response": "Hi there",
        "timestamp": datetime.utcnow()
    }

def test_chat_creation(chat_data):
    chat = Chat(**chat_data)
    assert chat.id == 1
    assert chat.user_id == 1
    assert chat.message == "Hello"
    assert chat.response == "Hi there"
    assert isinstance(chat.timestamp, datetime)

def test_chat_empty_message():
    invalid_data = {
        "id": 2,
        "user_id": 1,
        "message": "",
        "response": "Hi",
        "timestamp": datetime.utcnow()
    }
    with pytest.raises(ValueError):
        Chat(**invalid_data)