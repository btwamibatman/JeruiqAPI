from flask import Blueprint, request, jsonify
from core.ports.auth_service import AuthService
from core.use_cases.user_registration import UserRegistration
from core.use_cases.user_login import UserLogin
from core.ports.user_repository import UserRepository
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository

user_blueprint = Blueprint("users", __name__)

# Используем SQLAlchemy репозиторий пользователей
auth_service = JWTAuthService()
user_repo: UserRepository = SQLAlchemyUserRepository()
user_registration = UserRegistration(user_repo, auth_service)
user_login = UserLogin(user_repo, auth_service)


def token_required(f):
    """Декоратор для защиты маршрутов"""
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            token = token.split(" ")[1] 
            user_data = auth_service.verify_token(token)
            request.user = user_data  
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_blueprint.route("/", methods=["GET"])
@token_required
def get_users():
    users = user_repo.get_all_users()
    return jsonify([user.__dict__ for user in users])

@user_blueprint.route("/register", methods=["POST"])
def register_user():
    """Регистрация нового пользователя"""
    data = request.get_json()
    try:
        user = user_registration.register_user(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone_number=data["phone_number"]
        )
        return jsonify({"message": "User registered successfully", "user_id": user.user_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@user_blueprint.route("/login", methods=["POST"])
def login():
    """Авторизация пользователя"""
    data = request.get_json()
    try:
        token = user_login.login(email=data["email"], password=data["password"])
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
