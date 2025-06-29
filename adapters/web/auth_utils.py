from flask import request, jsonify, g # Import g for request context
from functools import wraps
import jwt
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
            # 1. Get token from Authorization header (Bearer token)
            print("DEBUG: Entered JWT decorator")
            auth_header = request.headers.get('Authorization', None)
            print(f"DEBUG: Authorization header: {auth_header}")
            if not auth_header or not auth_header.startswith('Bearer '):
                print("DEBUG: Invalid or missing Authorization header")
                return jsonify({"message": "Invalid Authorization header format!"}), 401
            token = auth_header.split(' ')[1]
            print(f"DEBUG: Extracted token: {token}")
            try:
                user_id = jwt_service.verify_token(token)
                print(f"DEBUG: user_id from token: {user_id}")
                if not user_id:
                    print("DEBUG: Invalid token or user_id missing")
                    return jsonify({"message": "Invalid token"}), 401
                repo = user_repository_factory()
                user = repo.get_by_id(user_id)
                print(f"DEBUG: User from repo: {user}")
                if not user:
                    print("DEBUG: User not found in DB")
                    return jsonify({"message": "User not found"}), 401
                g.current_user = user
                print("DEBUG: g.current_user set successfully")
            except jwt.ExpiredSignatureError:
                print("DEBUG: Token expired")
                return jsonify({"message": "Token expired"}), 401
            except Exception as e:
                print(f"DEBUG: Exception during JWT verification: {e}")
                return jsonify({"message": "Invalid token"}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator