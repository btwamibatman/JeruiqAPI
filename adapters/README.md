# Adapters Folder

The `adapters/` folder in the `JeruyiqAPI` project follows the clean architecture pattern, serving as the interface between the core business logic (`core/`, `domain/`) and external systems (e.g., databases, HTTP APIs, authentication mechanisms). Adapters implement the ports defined in `core/ports/`, enabling the application to interact with external dependencies while keeping the core logic isolated and independent.

## Purpose

The `adapters/` folder contains concrete implementations for:
- Authentication mechanisms (JWT, password hashing).
- Error handling for web and AI services.
- Data access to the database using SQLAlchemy.
- Data validation and serialization for API requests/responses.
- Middleware for Flask routes.

This structure ensures that external systems (e.g., Flask, PostgreSQL, `google-generativeai`) are abstracted away from the domain logic, making the application modular, testable, and maintainable.

## Directory Structure

- **`auth/`**: Authentication-related adapters.
  - `jwt_auth.py`: Implements JWT token generation and verification using `pyjwt`. Generates tokens with a configurable expiration (default: 7 days) and validates them, raising errors for expired or invalid tokens.
  - `password_hasher.py`: Handles password hashing and verification using `bcrypt`. Used for secure password storage during user registration and login.

- **`error_handlers/`**: Error handling logic for different parts of the application.
  - `ai_error_handlers.py`: Manages errors specific to the `google-generativeai` API (e.g., rate limits, API failures) used in `ai_service` for `gemini_ai_model.py`.
  - `error_handlers.py`: Generic error handler for Flask applications, handling `HTTPException` and uncaught exceptions, returning JSON responses with appropriate status codes.
  - `web_error_handlers.py`: Registers Flask-specific error handlers for HTTP errors (e.g., 404, 500, 400), ensuring consistent API responses.

- **`repositories/sqlalchemy/`**: Data access layer using SQLAlchemy for database operations.
  - `chat_repository.py`: Implements database operations (e.g., create, get_by_id) for the `Chat` model, mapping between `domain/models/chat.py` and `core/entities/chat.py`.
  - `permission_repository.py`: Handles database operations for the `Permission` model.
  - `role_repository.py`: Manages database operations for the `Role` model.
  - `user_repository.py`: Provides data access for the `User` model, including methods like `get_by_email`, `get_by_id`, and `save`.

- **`schemas/`**: Data validation and serialization schemas using `pydantic`.
  - `chat_schema.py`: Defines schemas for chat-related API requests/responses (e.g., message, response, timestamp).
  - `permission_schema.py`: Schemas for permission data (e.g., name, description).
  - `role_schema.py`: Schemas for role data (e.g., name, description).
  - `user_schema.py`: Schemas for user data (e.g., name, email, password, phone_number), with email validation using `EmailStr`.

- **`middleware.py`**: Flask middleware for JWT authentication.
  - Implements `require_jwt` to enforce JWT token validation on protected routes, integrating with `jwt_auth.py`.

## Usage

### Authentication
- **JWT Authentication**: Use `jwt_auth.py` in `api-gateway` and `user_service` for token generation and validation. Example:
  ```python
  from adapters.auth.jwt_auth import JWTAuthService

  jwt_service = JWTAuthService()
  token = jwt_service.generate_token(user_id="123", email="user@example.com")
  payload = jwt_service.verify_token(token)
  ```
- **Password Hashing**: Use `password_hasher.py` for secure password storage and verification. Example:
  ```python
  from adapters.auth.password_hasher import PasswordHasher

  hasher = PasswordHasher()
  hashed = hasher.hash_password("my_password")
  is_valid = hasher.verify_password("my_password", hashed)
  ```

### Error Handling
- **AI Errors**: Use `ai_error_handlers.py` in `ai_service` to handle `google-generativeai` errors. Example:
  ```python
  from adapters.error_handlers.ai_error_handlers import AIErrorHandler
  from google.api_core.exceptions import GoogleAPIError

  try:
      # Call to gemini_ai_model.py
      response = gemini_model.generate("prompt")
  except GoogleAPIError as e:
      error_response = AIErrorHandler.handle_google_api_error(e)
  ```
- **Web Errors**: Register `web_error_handlers.py` with your Flask app in `api-gateway` or `ai_service`. Example:
  ```python
  from adapters.error_handlers.web_error_handlers import register_error_handlers
  from flask import Flask

  app = Flask(__name__)
  register_error_handlers(app)
  ```
- **Generic Errors**: Use `error_handlers.py` as a fallback for uncaught exceptions in Flask routes.

### Data Access
- **Repositories**: Use the repositories in `user_service` and `ai_service` for database operations. Example:
  ```python
  from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository

  repo = SQLAlchemyUserRepository()
  user = repo.get_by_email("user@example.com")
  ```

### Schemas
- **Validation**: Use schemas in `api-gateway/routes/` and service routes for request/response validation. Example:
  ```python
  from adapters.schemas.user_schema import UserSchema

  data = {"name": "John", "email": "john@example.com", "password": "pass123", "phone_number": "1234567890"}
  user = UserSchema(**data)
  ```

### Middleware
- **JWT Protection**: Apply `require_jwt` to Flask routes requiring authentication. Example:
  ```python
  from adapters.middleware import require_jwt
  from flask import Blueprint

  bp = Blueprint("protected", __name__)

  @bp.route("/protected")
  @require_jwt
  def protected_route():
      return {"message": "Protected endpoint"}
  ```

## Testing

Unit tests for the `adapters/` folder are located in `tests/unit/adapters/`. To run tests:
```bash
pytest tests/unit/adapters/
```

### Test Coverage
- **`auth/`**: Tests for `jwt_auth.py` and `password_hasher.py` ensure token generation/validation and password hashing/verification work correctly.
- **`error_handlers/`**: Tests for `ai_error_handlers.py`, `error_handlers.py`, and `web_error_handlers.py` verify error handling for AI and web scenarios.
- **`repositories/sqlalchemy/`**: Tests for all repository files ensure database operations (e.g., create, get_by_id) function as expected.
- **`schemas/`**: Tests for schema validation are part of integration tests in `tests/integration/`.
- **`middleware.py`**: Tested as part of integration tests for `api-gateway` and `ai_service` routes.

## Dependencies

The `adapters/` folder relies on the following dependencies (listed in `requirements.txt`):
- `bcrypt`: For password hashing.
- `pyjwt`: For JWT token handling.
- `google-generativeai`: For AI error handling.
- `sqlalchemy`: For database operations.
- `pydantic`: For schema validation.
- `flask`: For web error handling and middleware.
- `python-dotenv`: For loading environment variables (e.g., `JWT_SECRET_KEY`).

## Contributing

To add or modify adapters:
1. Identify the external system or interface (e.g., new database, authentication method).
2. Define the corresponding port in `core/ports/` if needed.
3. Create or update the adapter in the appropriate subdirectory (e.g., `repositories/mongodb/` for a MongoDB adapter).
4. Add unit tests in `tests/unit/adapters/`.
5. Update this `README.md` to reflect changes.

## Notes

- Ensure environment variables (e.g., `JWT_SECRET_KEY`, `TOKEN_EXPIRATION_DAYS`) are set in your `.env` file for `jwt_auth.py`.
- The `gemini_ai_model.py` in `ai_service` relies on `ai_error_handlers.py` for robust error handling.
- The `middleware.py` assumes `Authorization` headers are in the format `Bearer <token>`.

Last updated: May 15, 2025