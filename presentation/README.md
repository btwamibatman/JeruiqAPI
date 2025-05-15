# Presentation Layer

The `presentation/` folder in the `JeruyiqAPI` project serves as the presentation layer, responsible for rendering frontend pages and handling API endpoints related to user interaction with the AI chat functionality. Built with Flask, it integrates with the `domain/services/ai_service/gemini_ai_model.py` for AI-driven chat responses and works alongside the `api_gateway/` for authentication and routing.

## Purpose

The presentation layer:
- **Frontend Rendering**: Serves HTML templates for the start page and chat interface.
- **Chat API**: Provides endpoints to create chat sessions and send messages, leveraging the `ChatSession` class from `ai_service`.
- **Integration**: Connects with the `adapters/` folder for authentication, data validation, and error handling.

## Directory Structure

- **`frontend.py`**: Defines the `frontend_bp` blueprint, rendering HTML templates for the `/` (start page) and `/chat` (chat page) routes.
- **`routes/`**:
  - `chat_routes.py`: Implements the `chat_bp` blueprint with `/create_session` (POST) and `/send_message` (POST) endpoints for managing chat sessions and sending messages to the AI.

## Setup and Installation

### Prerequisites
- Python 3.9+
- Flask (installed via `api_gateway/requirements.txt` or project-wide `requirements.txt`)

### Installation
1. Ensure the project dependencies are installed:
   ```bash
   pip install -r api_gateway/requirements.txt  # Or project-wide requirements
   ```
2. Verify the `templates/` folder contains `startpage.html` and `chat.html` (adjust `frontend.py` if the path differs).

## Usage

### Running Locally
1. Start the application (assuming integrated with `app.py` in `api_gateway/`):
   ```bash
   python api_gateway/app.py
   ```
2. Access the endpoints:
   - **Start Page**: `GET http://localhost:5000/` (renders `startpage.html`).
   - **Chat Page**: `GET http://localhost:5000/chat` (renders `chat.html`, requires authentication if enabled).
   - **Create Session**: `POST http://localhost:5000/create_session`
     ```json
     {}
     ```
     **Response**: `201 { "session_id": "uuid-string" }`
   - **Send Message**: `POST http://localhost:5000/send_message`
     ```json
     {
         "message": "Hello, how can you help?",
         "session_id": "uuid-string"
     }
     ```
     **Response**: `200 { "response": "AI response string" }`

### Authentication
- The `chat_routes.py` endpoints currently lack authentication. To secure them, integrate with `api_gateway/middleware.py` or `adapters/middleware.py` using the `@token_required` decorator.

## Testing

Unit and integration tests for the presentation layer are located in `tests/unit/presentation/` and `tests/integration/presentation/`. To run tests:
```bash
pytest tests/unit/presentation/
pytest tests/integration/presentation/
```

### Test Coverage
- **frontend.py**: Tests for template rendering success and failure cases.
- **chat_routes.py**: Tests for `/create_session` and `/send_message`, covering session creation, message handling, and error scenarios.

## Integration with Adapters

The presentation layer relies on the following `adapters/` components:
- **`auth/jwt_auth.py`**: For potential JWT token validation if authentication is added.
- **`schemas/chat_schema.py`**: For validating `send_message` request data.
- **`error_handlers/`**: For handling exceptions in route logic.
- **`repositories/sqlalchemy/chat_repository.py`**: For potential chat session persistence (if implemented).

## Notes

- **Template Location**: Ensure `templates/startpage.html` and `templates/chat.html` exist and are accessible. Adjust the `template_folder` path in `frontend.py` if necessary.
- **Session Management**: The `chat_sessions` dictionary is a temporary in-memory store. For production, use a persistent store (e.g., Redis or PostgreSQL via `chat_repository.py`).
- **Authentication**: Add `@token_required` to `chat_routes.py` endpoints to restrict access to authenticated users.
- **Frontend Integration**: The `chat.html` template should include JavaScript/AJAX to call `/send_message` and display responses, using the session ID from `/create_session`.

## Contributing

To extend the presentation layer:
1. Add new routes or templates in `frontend.py` or `routes/`.
2. Secure endpoints with the `@token_required` decorator from `api_gateway/middleware.py`.
3. Update `chat_routes.py` to integrate with a persistent session store if needed.
4. Add unit tests in `tests/unit/presentation/` and integration tests in `tests/integration/presentation/`.
5. Update this `README.md` with new endpoint or template details.

Last updated: May 15, 2025