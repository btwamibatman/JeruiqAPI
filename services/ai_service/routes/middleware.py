from functools import wraps
from flask import request, jsonify
import requests
import os

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            response = requests.post(f"{AUTH_SERVICE_URL}/auth/validate-token", headers={"Authorization": token})
            if response.status_code != 200:
                return jsonify({"message": "Token is invalid"}), 401

            return f(response.json(), *args, **kwargs)
        except requests.RequestException:
            return jsonify({"message": "Auth service unavailable"}), 503
    return decorated
