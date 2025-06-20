import logging
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from adapters.auth.password_hasher import PasswordHasher
from core.use_cases.user_registration import UserRegistration
from core.use_cases.user_login import UserLogin
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository

auth_blueprint = Blueprint("auth", __name__)

# Initialize services
auth_service = JWTAuthService()
user_repo: UserRepository = SQLAlchemyUserRepository()
user_registration = UserRegistration(user_repo, auth_service)
user_login = UserLogin(user_repo, auth_service)

@auth_blueprint.route("/register", methods=["POST"])
def register_user():
    """Register a new user"""
    data = request.get_json()

    required_fields = ["name", "email", "password", "phone_number"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Check if user already exists
        if user_repo.get_by_email(data["email"]):
            return jsonify({"error": "Email already registered"}), 400

        # Hash password
        hashed_password = generate_password_hash(data["password"])

        # Вызываем регистрацию без передачи user_id – он создастся внутри конструктора User
        user = user_registration.register_user(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone_number=data["phone_number"]
        )

        logging.info(f"User {data['email']} registered successfully.")
        return jsonify({
            "message": "User registered successfully",
            "user_id": user.user_id
        }), 201

    except Exception as e:
        logging.error(f"Registration error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """User login"""
    data = request.get_json()

    if not all(k in data for k in ["email", "password"]):
        return jsonify({"error": "Email and password required"}), 400

    try:
        user = user_repo.get_by_email(data["email"])
        if not user or not PasswordHasher.verify_password(data["password"], str(user.password_hash)):
            return jsonify({"error": "Invalid email or password"}), 401
        # Generate JWT token
        token = auth_service.generate_token(user.user_id, user.email)

        logging.info(f"User {data['email']} logged in successfully.")
        return jsonify({"access_token": token}), 200

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
