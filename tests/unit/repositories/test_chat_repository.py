import pytest
from unittest.mock import MagicMock
from adapters.repositories.sqlalchemy.chat_repository import ChatRepository  # Adjust import
from domain.models.chat import Chat
from sqlalchemy.orm import Session
from datetime import datetime

@pytest.fixture
def mock_session():
    return MagicMock(spec=Session)

def test_create_chat(mock_session):
    repo = ChatRepository(mock_session)
    chat = Chat(id=1, user_id=1, message="Hello", response="Hi", timestamp=datetime.utcnow())
    
    repo.create(chat)
    
    mock_session.add.assert_called_with(chat)
    mock_session.commit.assert_called_once()

def test_get_by_id(mock_session):
    repo = ChatRepository(mock_session)
    chat = Chat(id=1, user_id=1, message="Hello", response="Hi", timestamp=datetime.utcnow())
    mock_session.query.return_value.filter.return_value.first.return_value = chat
    
    result = repo.get_by_id(1)
    
    assert result == chat
    mock_session.query.assert_called_with(Chat)