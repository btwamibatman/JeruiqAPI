from flask import Blueprint, request, jsonify
from core.use_cases.user_login import UserLogin
from core.ports.auth_service import AuthService
from adapters.auth.jwt_auth import JWTAuthService
from adapters.repositories.sqlalchemy.user_repository import SQLAlchemyUserRepository

auth_blueprint = Blueprint("auth", __name__)

# Используем репозиторий пользователей и сервис аутентификации
user_repo = SQLAlchemyUserRepository()
auth_service: AuthService = JWTAuthService()
user_login = UserLogin(user_repo)

@auth_blueprint.route("/login", methods=["POST"])
def login():
    """Авторизация пользователя и выдача JWT токена"""
    data = request.get_json()
    try:
        token = user_login.login(email=data["email"], password=data["password"])
        return jsonify({"token": token}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@auth_blueprint.route("/verify", methods=["GET"])
def verify_token():
    """Проверяет валидность токена"""
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is missing"}), 401

    try:
        user_data = auth_service.verify_token(token.split(" ")[1])  # Убираем "Bearer"
        return jsonify({"user": user_data}), 200
    except Exception as e:
        return jsonify({"error": "Invalid token"}), 401
