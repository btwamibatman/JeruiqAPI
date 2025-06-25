from flask import request, jsonify, g # Import g for request context
from functools import wraps
# Import dependencies needed by the decorator
from application.services.jwt_service import JWTService
from infrastructure.db.repositories.user_repository import UserRepository
from infrastructure.db.db import SessionLocal # Import session factory

# Define a factory function that accepts dependencies and returns the decorator
def jwt_required(jwt_service: JWTService, user_repository_factory):
    """
    Decorator factory to create a JWT authentication decorator.
    Accepts JWTService and a factory function for UserRepository.
    """
    def decorator(f):
        """
        The actual decorator function.
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """
            The wrapper function that performs JWT check.
            """
            token = None
            # 1. Get token from Authorization header (Bearer token)
            auth_header = request.headers.get('Authorization')
            if auth_header:
                parts = auth_header.split()
                if parts[0].lower() == 'bearer' and len(parts) == 2:
                    token = parts[1]
            # 2. If not in header, check cookie (if you chose that approach)
            #    Note: Using HttpOnly cookies is generally more secure for web browsers
            #    than storing JWT in localStorage and sending via Authorization header.
            #    Choose one approach based on your frontend strategy.
            if token is None:
                 token = request.cookies.get('jwt_token')

            if not token:
                # Token is missing from both header and cookie
                return jsonify({"message": "Authentication token is missing!"}), 401 # Unauthorized

            # 3. Verify token and get user ID
            user_id = jwt_service.verify_token(token)

            if user_id is None:
                # Token is invalid or expired
                return jsonify({"message": "Token is invalid or expired!"}), 401 # Unauthorized

            # 4. Get user from repository (optional but recommended)
            #    Need a DB session for the repository.
            #    Using a factory function passed via DI to get a new repo instance with a session.
            db_session = SessionLocal() # Get a new session for this request
            try:
                user_repository = UserRepository(db_session=db_session)
                current_user = user_repository.get_by_id(user_id)

                if current_user is None:
                    # Token is valid, but user doesn't exist (e.g., deleted from DB)
                    return jsonify({"message": "User not found!"}), 401 # Unauthorized

                # 5. Attach user to request context (g)
                #    The route function can now access the authenticated user via g.current_user
                g.current_user = current_user

            except Exception as e:
                 # Handle potential DB errors during user lookup
                 print(f"Error fetching user in JWT decorator: {e}")
                 # Return a generic error to the client for security
                 return jsonify({"message": "An error occurred during authentication."}), 500
            finally:
                 # Ensure the database session is closed
                 db_session.close()

            # If authentication succeeds, call the original route function
            return f(*args, **kwargs)

        return decorated_function
    return decorator