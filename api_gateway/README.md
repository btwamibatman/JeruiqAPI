# API Gateway

The `api_gateway/` folder is the entry point for the `JeruyiqAPI` project, a microservices-based application built with Flask. It acts as a reverse proxy, routing incoming HTTP requests to the appropriate microservices (`user_service`, `ai_service`), handles user authentication, and provides a health check endpoint for monitoring.

## Purpose

The API Gateway serves the following key functions:
- **Routing**: Forwards requests to microservices (`user_service` for user operations, `ai_service` for AI-related functionality like chat).
- **Authentication**: Manages user registration and login, issuing JWT tokens for secure access.
- **Authorization**: Protects routes with JWT token validation using middleware.
- **Health Monitoring**: Provides a health check endpoint to verify the API Gateway's status.
- **Error Handling**: Registers consistent error handlers for HTTP and application errors.

The API Gateway integrates with the `adapters/` folder for authentication (`jwt_auth.py`), data access (`user_repository.py`), and error handling (`web_error_handlers.py`).

## Directory Structure

- **`app.py`**: The main Flask application. Initializes the app, sets up logging, registers error handlers, and mounts blueprints for routing.
- **`requirements.txt`**: Lists dependencies required to run the API Gateway.
- **`Dockerfile`**: Defines the Docker image configuration for building and deploying the API Gateway.
- **`middleware.py`**: Implements the `token_required` middleware for JWT token validation, used to secure routes by calling an external auth service.
- **`routes/`**: Contains Flask blueprints for different API endpoints.
  - `ai_routes.py`: Handles AI-related routes (`/ai/chat`, `/ai/sessions/<session_id>`), proxying requests to `ai_service`.
  - `auth_routes.py`: Manages authentication routes (`/register`, `/login`) for user registration and login.
  - `user_routes.py`: Provides user-related routes (`/me`) to fetch the authenticated user's profile.
  - `health_check.py`: Implements a health check endpoint (`/health`) to monitor the API Gateway's status.

## Setup and Installation

### Prerequisites
- Python 3.9+
- Docker (for containerized deployment)

### Installation
1. Clone the repository and navigate to the `api_gateway/` folder:
   ```bash
   cd api_gateway/
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the required environment variables:
   ```
   AUTH_SERVICE_URL=http://auth-service:5001
   AI_SERVICE_URL=http://ai-service:5003
   JWT_SECRET_KEY=your-secret-key-here
   TOKEN_EXPIRATION_DAYS=7
   ```

## Usage

### Running Locally
1. Start the application:
   ```bash
   python app.py
   ```
   The API Gateway will run on `http://0.0.0.0:5000`.

2. Access the endpoints:
   - **Register a User**: `POST http://localhost:5000/register`
     ```json
     {
         "name": "John Doe",
         "email": "john@example.com",
         "password": "securepassword123",
         "phone_number": "1234567890"
     }
     ```
   - **Login**: `POST http://localhost:5000/login`
     ```json
     {
         "email": "john@example.com",
         "password": "securepassword123"
     }
     ```
   - **Get User Profile**: `GET http://localhost:5000/me` (requires `Authorization: Bearer <token>`)
   - **Chat with AI**: `POST http://localhost:5000/ai/chat` (requires `Authorization: Bearer <token>`)
     ```json
     {
         "message": "Hello, how can you help me?"
     }
     ```
   - **Clear Chat Session**: `DELETE http://localhost:5000/ai/sessions/<session_id>` (requires `Authorization: Bearer <token>`)
   - **Health Check**: `GET http://localhost:5000/health`

### Running in Production
Use `gunicorn` for production deployment:
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

## API Endpoints

### Authentication
- **`POST /register`**: Register a new user. Returns the user ID on success.
  - **Request Body**: `{ "name": string, "email": string, "password": string, "phone_number": string }`
  - **Response**: `201 { "message": "User registered successfully", "user_id": string }` or `400 { "error": string }`
- **`POST /login`**: Log in a user and return a JWT token.
  - **Request Body**: `{ "email": string, "password": string }`
  - **Response**: `200 { "access_token": string }` or `401 { "error": string }`

### User
- **`GET /me`**: Fetch the authenticated user's profile (requires JWT).
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: `200 { "user_id": string, "name": string, "email": string, "phone_number": string, "role": string }` or `401 { "error": string }`

### AI
- **`POST /ai/chat`**: Send a chat message to `ai_service` (requires JWT).
  - **Headers**: `Authorization: Bearer <token>`
  - **Request Body**: `{ "message": string }`
  - **Response**: `200 { "response": string }` or `503 { "message": "AI service unavailable" }`
- **`DELETE /ai/sessions/<session_id>`**: Clear a chat session in `ai_service` (requires JWT).
  - **Headers**: `Authorization: Bearer <token>`
  - **Response**: `200 { "message": string }` or `503 { "message": "AI service unavailable" }`

### Health
- **`GET /health`**: Check the API Gateway's health status.
  - **Response**: `200 { "status": "healthy", "service": "api-gateway", "version": "1.0.0" }`

## Testing

Integration tests for the API Gateway are located in `tests/integration/api_gateway/`. To run tests:
```bash
pytest tests/integration/api_gateway/
```

### Test Coverage
- **Authentication**: Tests for `/register` and `/login` endpoints, covering successful and failed scenarios.
- **User Routes**: Tests for `/me`, ensuring proper token validation and user data retrieval.
- **AI Routes**: Tests for `/ai/chat` and `/ai/sessions/<session_id>`, verifying proxying to `ai_service`.
- **Health Check**: Tests for `/health`, confirming the endpoint returns the correct status.

## Deployment

### Docker
The API Gateway is designed to run in a Docker container. Build and run the image:
1. Build the Docker image:
   ```bash
   docker build -t jeruyiq-api-gateway .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env jeruyiq-api-gateway
   ```

### Docker Compose (Recommended for Microservices)
To deploy with other services (`user_service`, `ai_service`), use Docker Compose:
```yaml
version: '3.8'
services:
  api-gateway:
    image: jeruyiq-api-gateway
    build: ./api_gateway
    ports:
      - "5000:5000"
    env_file:
      - .env
    depends_on:
      - auth-service
      - ai-service
  auth-service:
    # Configuration for auth_service
  ai-service:
    # Configuration for ai_service
```

## Dependencies

The API Gateway relies on the following dependencies (listed in `requirements.txt`):
- `Flask==2.2.5`: Web framework for building the API.
- `requests==2.31.0`: For making HTTP requests to microservices.
- `python-dotenv==1.0.0`: For loading environment variables from a `.env` file.
- `gunicorn==21.2.0`: WSGI server for production deployment.
- `pyjwt==2.8.0`, `bcrypt==4.1.2`, `sqlalchemy==2.0.23`, `pydantic==2.5.2`, `psycopg2-binary==2.9.9`: For integration with `adapters/` (authentication, data access, schema validation).

## Configuration

### Environment Variables
- `AUTH_SERVICE_URL`: URL of the auth service (default: `http://localhost:5001`).
- `AI_SERVICE_URL`: URL of the AI service (default: `http://localhost:5003`).
- `JWT_SECRET_KEY`: Secret key for JWT token generation/validation.
- `TOKEN_EXPIRATION_DAYS`: Number of days before a JWT token expires (default: 7).

Ensure these are set in your `.env` file or passed as environment variables in your deployment.

## Integration with Adapters

The API Gateway uses the following components from the `adapters/` folder:
- **`auth/jwt_auth.py`**: For JWT token generation and validation in `auth_routes.py` and `user_routes.py`.
- **`repositories/sqlalchemy/user_repository.py`**: For database operations in `auth_routes.py` and `user_routes.py`.
- **`error_handlers/web_error_handlers.py`**: Registers error handlers for consistent HTTP error responses.
- **`schemas/`**: Uses `UserSchema` and `ChatSchema` for input/output validation.

## Notes

- **Token Format**: The `Authorization` header must be in the format `Bearer <token>`.
- **Error Handling**: The API Gateway uses `adapters/error_handlers/web_error_handlers.py` to ensure consistent error responses.
- **Microservices Dependency**: Ensure `auth_service` and `ai_service` are running and accessible at the URLs specified in `AUTH_SERVICE_URL` and `AI_SERVICE_URL`.
- **Security**: Avoid running with `debug=True` in production, as it can expose sensitive information.
- **Versioning**: The health check endpoint includes a version (`1.0.0`), which should be updated with each release.

## Contributing

To add new routes or features:
1. Create a new blueprint in `routes/` (e.g., `new_routes.py`).
2. Register the blueprint in `app.py`.
3. Add middleware for authentication if needed (using `middleware.py`).
4. Update this `README.md` with the new endpoint details.
5. Add integration tests in `tests/integration/api_gateway/`.

Last updated: May 15, 2025