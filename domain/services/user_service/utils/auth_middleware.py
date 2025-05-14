from functools import wraps
from flask import request, jsonify
import requests
import os
import logging

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")

logger = logging.getLogger(__name__)

def token_required(f):
    """Middleware to ensure the request has a valid authentication token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token or not token.startswith("Bearer "):
            return jsonify({"message": "Token is missing or invalid"}), 401
        
        token = token.split(" ")[1]  # Extract token
        
        try:
            response = requests.post(
                f"{AUTH_SERVICE_URL}/auth/validate-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                return jsonify({"message": "Token is invalid"}), 401
            
            return f(response.json(), *args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Error communicating with auth service: {e}")
            return jsonify({"message": "Auth service unavailable"}), 503
    return decorated