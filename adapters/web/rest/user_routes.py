import logging
from flask import Blueprint, request, jsonify
from core.ports.auth_service import AuthService
from core.use_cases.user_registration import UserRegistration
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository

user_blueprint = Blueprint("users", __name__)

# Initialize services
auth_service = JWTAuthService()
user_repo: UserRepository = SQLAlchemyUserRepository()
user_registration = UserRegistration(user_repo, auth_service)

def token_required(f):
    """Decorator for protecting routes"""
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Valid Bearer token is required"}), 401

        token = auth_header.split(" ")[1]
        try:
            user_data = auth_service.verify_token(token)
            request.user = user_data
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            logging.error(f"Unexpected error during token verification: {str(e)}")
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_blueprint.route("/me", methods=["GET"])
@token_required
def get_user_profile():
    """Get current user's profile"""
    try:
        user = user_repo.get_by_id(request.user["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number
        }), 200
    except Exception as e:
        logging.error(f"Error fetching user profile: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
