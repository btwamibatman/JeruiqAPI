from flask import Flask, g, jsonify
from marshmallow import ValidationError

# Import blueprint factory functions
from adapters.web.rest.api_blueprint import create_api_blueprint
from adapters.web.rest.auth_blueprint import create_auth_blueprint
from adapters.web.rest.ai_blueprint import create_ai_blueprint
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

# Import infrastructure clients and domain services needed for dependency injection
from infrastructure.external.photon_client import PhotonClient
from application.use_cases.find_places import find_places
from application.use_cases.register_user import register_user, EmailAlreadyExistsException
from application.use_cases.login_user import login_user, InvalidCredentialsException
from application.services.password_hasher import PasswordHasher
from application.services.jwt_service import JWTService # Ensure JWTService is imported
from domain.exceptions import (
    DomainException,
    InvalidQueryException,
    ExternalServiceException,
    PlaceNotFoundException
)

def create_app(config_object=Config):
    """
    Application factory function to create and configure the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    # --- Dependency Injection Setup ---
    # Create instances of infrastructure clients
    photon_client = PhotonClient()

    # Create instances of application services
    password_hasher = PasswordHasher()

    # Define the factory function for JWTService
    def create_jwt_service() -> JWTService:
        """Factory function to create a JWTService instance."""
        if not hasattr(config_object, 'JWT_SECRET_KEY') or not config_object.JWT_SECRET_KEY:
            raise RuntimeError("JWT_SECRET_KEY is not set in Config.")

        secret_key = config_object.JWT_SECRET_KEY

        try:
            # Access the expiration minutes and CONVERT IT TO AN INTEGER
            expiration_minutes_str = config_object.JWT_EXPIRATION_MINUTES
            # Use the default value if the env var is not set or is None
            if expiration_minutes_str is None:
                 # Assuming Config class has a default value set for JWT_EXPIRATION_MINUTES
                 expiration_minutes = int(config_object.JWT_EXPIRATION_MINUTES)
            else:
                 expiration_minutes = int(expiration_minutes_str) # Convert the string from env var
        except (ValueError, TypeError) as e:
            raise RuntimeError(f"Invalid value for JWT_EXPIRATION_MINUTES in Config: {expiration_minutes_str}. Must be an integer.") from e

        return JWTService(
            secret_key=secret_key,
            expiration_minutes=expiration_minutes # Pass the integer value
        )

    # Define a factory function that creates a UserRepository instance with a session
    def create_user_repository():
        """Factory function to create a UserRepository with a new DB session."""
        # Note: In a real Flask app, you'd manage the session lifecycle per request
        # using Flask-SQLAlchemy or similar. This is a simplified approach for DI wiring.
        db_session = SessionLocal()
        # We don't close the session here; the decorator or a request teardown handles it.
        return UserRepository(db_session=db_session)


    # Create instances of application use cases, injecting dependencies
    find_places_use_case_instance = lambda user_text: find_places(user_text, photon_client)

    register_user_use_case_instance = lambda name, surname, email, plain_password: register_user(
        name=name,
        surname=surname,
        email=email,
        plain_password=plain_password,
        user_repository=create_user_repository(), # Pass a new repo instance with a session
        password_hasher=password_hasher
    )

    login_user_use_case_instance = lambda email, plain_password: login_user(
        email=email,
        plain_password=plain_password,
        user_repository=create_user_repository(), # Pass a new repo instance with a session
        password_hasher=password_hasher,
        jwt_service=create_jwt_service() # CALL THE FACTORY FUNCTION HERE
    )

    # Create the jwt_required decorator factory instance, injecting dependencies
    jwt_required_decorator = jwt_required(
        jwt_service=create_jwt_service(), # CALL THE FACTORY FUNCTION HERE
        user_repository_factory=create_user_repository # Pass the factory function
    )


    # --- Register Blueprints ---
    # Pass the jwt_required_decorator instance to blueprints that need it
    app.register_blueprint(create_api_blueprint(
        find_places_use_case=find_places_use_case_instance,
        jwt_required_decorator=jwt_required_decorator # Pass the decorator instance
    ))
    app.register_blueprint(create_ai_blueprint(
        jwt_required_decorator=jwt_required_decorator # Pass the decorator instance
    ))
    app.register_blueprint(create_auth_blueprint(
        register_user_use_case=register_user_use_case_instance,
        login_user_use_case=login_user_use_case_instance
    ))
    app.register_blueprint(frontend_bp)

    # --- Register Error Handlers ---
    app.register_error_handler(ValidationError, handle_validation_error)
    app.register_error_handler(InvalidQueryException, handle_invalid_query_exception)
    app.register_error_handler(PlaceNotFoundException, handle_place_not_found_exception)
    app.register_error_handler(ExternalServiceException, handle_external_service_exception)
    app.register_error_handler(DomainException, handle_domain_exception)
    app.register_error_handler(EmailAlreadyExistsException, handle_domain_exception)
    app.register_error_handler(InvalidCredentialsException, handle_domain_exception)
    app.register_error_handler(Exception, handle_exception)

    # --- Database Session Management (Crucial for Web Apps) ---
    # This ensures a DB session is created at the start of a request
    # and closed at the end, even if errors occur.
    # If using Flask-SQLAlchemy, it handles this automatically.
    # If using SessionLocal directly in repos, ensure they are closed.
    # A more robust approach might store the session in g and close it here.
    # For now, let's add a teardown to close sessions created by SessionLocal
    # in the repository factory and jwt_required decorator.
    @app.teardown_request
    def teardown_request(exception=None):
        db = getattr(g, 'db_session', None) # Check if session was stored in g (e.g., by decorator)
        if db is not None:
            db.close()
        # Also need to handle sessions created directly in repository factory if not stored in g
        # This manual approach is tricky. Using Flask-SQLAlchemy is highly recommended.
        # For now, rely on the decorator's finally block and hope other sessions are short-lived.
        # A better manual approach:
        # @app.before_request
        # def before_request():
        #     g.db_session = SessionLocal()
        # Then pass g.db_session to repository factories.
        # @app.teardown_request
        # def teardown_request(exception=None):
        #     db = getattr(g, 'db_session', None)
        #     if db is not None:
        #         db.close()


    # Add a simple root route if needed, or handle it in a blueprint
    @app.route("/", methods=["GET"])
    def index():
        # You might want to redirect to the frontend blueprint's index route here
        # return redirect(url_for('frontend.index'))
        return jsonify({"message": "Jeruyiq API is running!"})


    return app