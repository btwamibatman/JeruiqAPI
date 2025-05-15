import logging
from flask import Blueprint, request, jsonify
from core.ports.auth_service import AuthService
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository
from api_gateway.middleware import token_required

user_bp = Blueprint("users", __name__)

# Initialize services
auth_service = JWTAuthService()
user_repo: UserRepository = SQLAlchemyUserRepository()

@user_bp.route("/me", methods=["GET"])
def get_user_profile(current_user):
    try:
        user = user_repo.get_by_id(current_user["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({
            "user_id": str(user.user_id),
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role
        }), 200
    except Exception as e:
        logging.error(f"Error fetching user profile: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500