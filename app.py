from flask import Flask, request, jsonify, g
from marshmallow import ValidationError
# Import blueprint factory functions
from adapters.web.rest.api_blueprint import create_api_blueprint
from adapters.web.rest.ai_blueprint import create_ai_blueprint
from adapters.web.rest.auth_blueprint import create_auth_blueprint
# Import specific error handlers
from adapters.web.error_handlers import (
    handle_exception,
    handle_validation_error,
    handle_invalid_query_exception,
    handle_place_not_found_exception,
    handle_external_service_exception,
    handle_domain_exception
)
# Import the decorator factory
from adapters.web.auth_utils import jwt_required
# Import DB session factory and repository
from infrastructure.db.db import SessionLocal
from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.config import Config # Ensure Config is imported
from routes.frontend import frontend_bp
import os

# Import infrastructure clients and domain services needed for dependency injection
from infrastructure.external.gemini_client import GeminiClient
from infrastructure.external.photon_client import PhotonClient
from domain.services.ai_service.gemini_query_service import GeminiQueryService
from application.use_cases.find_places import find_places
from application.use_cases.register_user import register_user, EmailAlreadyExistsException
from application.use_cases.login_user import login_user, InvalidCredentialsException
from application.services.chat_session_manager import ChatSessionManager
from application.services.password_hasher import PasswordHasher
from application.services.jwt_service import JWTService # Ensure JWTService is imported
from domain.exceptions import (
    DomainException,
    InvalidQueryException,
    ExternalServiceException,
    PlaceNotFoundException
)

# --- Dependency Injection Setup ---
# Create instances of infrastructure clients
gemini_client = GeminiClient()
photon_client = PhotonClient()

# Create instances of domain services, injecting infrastructure clients
gemini_service = GeminiQueryService(gemini_client=gemini_client)
# search_service = SearchService(...)

# Create instances of application services
chat_session_manager = ChatSessionManager()
password_hasher = PasswordHasher()

# Define the factory function for JWTService (keep this function)
def create_jwt_service() -> JWTService:
    """Factory function to create a JWTService instance."""
    # Ensure JWT_SECRET_KEY is in your Config (good check)
    if not hasattr(Config, 'JWT_SECRET_KEY') or not Config.JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not set in Config.")

    # Access the secret key
    secret_key = Config.JWT_SECRET_KEY

    # Access the expiration minutes and CONVERT IT TO AN INTEGER
    # Use a try-except block in case the environment variable is not a valid number
    try:
        expiration_minutes_str = Config.JWT_EXPIRATION_MINUTES
        # Ensure the value is not None before converting
        if expiration_minutes_str is None:
             # Use the default value if the env var is not set
             expiration_minutes = int(Config.JWT_EXPIRATION_MINUTES) # This will use the default '1'
        else:
             expiration_minutes = int(expiration_minutes_str) # Convert the string from env var
    except (ValueError, TypeError) as e:
        raise RuntimeError(f"Invalid value for JWT_EXPIRATION_MINUTES in Config: {expiration_minutes_str}. Must be an integer.") from e


    return JWTService(
        secret_key=secret_key,
        expiration_minutes=expiration_minutes # Pass the integer value
    )

# Create DB session factory (SessionLocal is already the factory)
# Define a factory function that creates a UserRepository instance with a session
def create_user_repository():
    """Factory function to create a UserRepository with a new DB session."""
    # Note: In a real Flask app, you'd manage the session lifecycle per request
    # using Flask-SQLAlchemy or similar. This is a simplified approach for DI wiring.
    db_session = SessionLocal()
    # We don't close the session here; the decorator or a request teardown handles it.
    return UserRepository(db_session=db_session)



# Create instances of application use cases, injecting dependencies
find_places_use_case_instance = lambda user_text: find_places(user_text, gemini_service, photon_client)

# The register_user use case needs UserRepository and PasswordHasher
register_user_use_case_instance = lambda name, surname, email, plain_password: register_user(
    name=name,
    surname=surname,
    email=email,
    plain_password=plain_password,
    user_repository=create_user_repository(), # Pass a new repo instance with a session
    password_hasher=password_hasher
)

# The login_user use case needs UserRepository, PasswordHasher, and JWTService
# Use the factory function to create the JWTService instance here
login_user_use_case_instance = lambda email, plain_password: login_user(
    email=email,
    plain_password=plain_password,
    user_repository=create_user_repository(), # Pass a new repo instance with a session
    password_hasher=password_hasher,
    jwt_service=create_jwt_service() # <-- CALL THE FACTORY FUNCTION HERE
)

# Create the jwt_required decorator factory instance, injecting dependencies
# This instance will be passed to blueprints that need to protect routes
# Use the factory function to create the JWTService instance here as well
jwt_required_decorator = jwt_required(
    jwt_service=create_jwt_service(), # <-- CALL THE FACTORY FUNCTION HERE
    user_repository_factory=create_user_repository # Pass the factory function
)


# --- Flask App Creation ---
app = Flask(__name__)
app.config.from_object(Config) # Keep this line

# Register blueprints, using the factory functions and injecting dependencies
# Pass the jwt_required_decorator instance to blueprints that need it
app.register_blueprint(create_api_blueprint(
    find_places_use_case=find_places_use_case_instance,
    jwt_required_decorator=jwt_required_decorator # Pass the decorator instance
))
# AI blueprint might also need it if chat is only for logged-in users
app.register_blueprint(create_ai_blueprint(
    session_manager=chat_session_manager,
    jwt_required_decorator=jwt_required_decorator # Pass the decorator instance
))
# Auth blueprint does NOT need the decorator as its routes are for authentication itself
app.register_blueprint(create_auth_blueprint(
    register_user_use_case=register_user_use_case_instance,
    login_user_use_case=login_user_use_case_instance
))
app.register_blueprint(frontend_bp)

# Register specific error handlers (ensure they are imported)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_error_handler(InvalidQueryException, handle_invalid_query_exception)
app.register_error_handler(PlaceNotFoundException, handle_place_not_found_exception)
app.register_error_handler(ExternalServiceException, handle_external_service_exception)
app.register_error_handler(DomainException, handle_domain_exception) # Catch generic domain errors
# Register specific auth exceptions (can use generic handler or create specific ones)
app.register_error_handler(EmailAlreadyExistsException, handle_domain_exception)
app.register_error_handler(InvalidCredentialsException, handle_domain_exception)
app.register_error_handler(Exception, handle_exception) # Catch all other exceptions

# --- Database Session Management (Crucial for Web Apps) ---
# This ensures a DB session is created at the start of a request
# and closed at the end, even if errors occur.
@app.before_request
def before_request():
    # You might not need this if your repository factory handles sessions per call,
    # but a request-scoped session is more efficient.
    # If using Flask-SQLAlchemy, it handles this automatically.
    # If using SessionLocal directly in repos, ensure they are closed.
    pass # Placeholder - adjust based on your final session management strategy

@app.teardown_request
def teardown_request(exception=None):
    # Ensure the session created by SessionLocal() is closed.
    # If using Flask-SQLAlchemy, it handles this.
    # If using SessionLocal directly in the decorator/repo factory,
    # the decorator's finally block handles it for that specific use.
    # A more robust approach might store the session in g and close it here.
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Example of storing session in g (alternative to creating in decorator/repo factory)
# @app.before_request
# def before_request():
#     g._database = SessionLocal()
#
# @app.teardown_request
# def teardown_request(exception=None):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
# Then modify create_user_repository to use g.get('_database')


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Jeruyiq API!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG) # Use the port variable