from flask import Blueprint, request, Response, jsonify
import requests
import os
from .middleware import token_required  # Import authentication middleware

auth_bp = Blueprint('auth', __name__)
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/register", json=request.json)
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "Auth service unavailable"}), 503

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/login", json=request.json)
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "Auth service unavailable"}), 503