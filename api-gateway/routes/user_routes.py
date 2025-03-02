from flask import Blueprint, request, Response, jsonify
import requests
import os
from .middleware import token_required  # Import authentication middleware

user_bp = Blueprint('user', __name__)
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")

@user_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        response = requests.get(f"{USER_SERVICE_URL}/users", headers={"Authorization": f"Bearer {token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "User service unavailable"}), 503

@user_bp.route('/users/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}", headers={"Authorization": f"Bearer {token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "User service unavailable"}), 503
