import pytest
import logging
from adapters.error_handlers.error_handlers import ErrorHandler  # Adjust import

@pytest.fixture
def error_handler():
    return ErrorHandler()

def test_handle_generic_exception(error_handler, caplog):
    caplog.set_level(logging.ERROR)
    try:
        raise ValueError("Test error")
    except ValueError as e:
        result = error_handler.handle_exception(e)
    
    assert result == {"error": "Internal server error", "status": 500}
    assert "Test error" in caplog.text

def test_handle_value_error(error_handler, caplog):
    caplog.set_level(logging.ERROR)
    try:
        raise ValueError("Invalid input")
    except ValueError as e:
        result = error_handler.handle_exception(e)
    
    assert result == {"error": "Invalid input", "status": 400}
    assert "Invalid input" in caplog.text