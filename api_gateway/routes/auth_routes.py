import logging
from flask import Blueprint, request, jsonify
from core.use_cases.user_registration import UserRegistration
from core.use_cases.user_login import UserLogin
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository
from adapters.schemas.user_schema import UserCreateSchema, UserResponseSchema
from domain.services.user_service.user_service import UserService
from infrastructure.config import ActiveConfig
import datetime

# Initialize services and repository
auth_service = JWTAuthService()
user_repo: UserRepository = SQLAlchemyUserRepository()
user_registration = UserRegistration(user_repo, auth_service)
user_login = UserLogin(user_repo, auth_service)

# Configure logging
logging.basicConfig(level=ActiveConfig.LOG_LEVEL)
logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        user_data = UserCreateSchema(**data)
        if user_repo.get_by_email(user_data.email):
            return jsonify({"error": "Email already registered"}), 400

        user = user_registration.execute(
            email=user_data.email,
            password=user_data.password,  # Already hashed by UserCreateSchema
            name=user_data.name,
            phone_number=user_data.phone_number
        )
        logger.info(f"User {user_data.email} registered successfully at {datetime.datetime.now()}")
        user_response = UserResponseSchema.from_orm(user)
        return jsonify({"message": "User registered successfully", "user": user_response.dict()}), 201
    except ValueError as e:
        logger.warning(f"Registration failed for email {data.get('email', 'unknown')}: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Registration error for email {data.get('email', 'unknown')}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """User login endpoint"""
    data = request.get_json()
    if not data or not all(k in data for k in ["email", "password"]):
        return jsonify({"error": "Email and password are required"}), 400

    try:
        user = user_repo.get_by_email(data["email"])
        if not user or not UserService.verify_password(user, data["password"]):
            logger.warning(f"Login failed for email {data['email']}: Invalid credentials")
            return jsonify({"error": "Invalid email or password"}), 401
        token = auth_service.generate_token(user.user_id, user.email)

        logger.info(f"User {data['email']} logged in successfully at {datetime.datetime.now()}")
        user_response = UserResponseSchema.from_orm(user)
        response = {"access_token": token, "user": user_response.dict()}
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Login error for email {data.get('email', 'unknown')}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500