from functools import wraps
from flask import request, jsonify
import requests
import os
import logging
logger = logging.getLogger(__name__)

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if not auth_header.startswith("Bearer "):
                return jsonify({'message': 'Invalid Authorization header format'}), 401
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            response = requests.post(f"{AUTH_SERVICE_URL}/auth/validate-token", headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                logger.warning(f"Token validation failed for token: {token}")
                return jsonify({'message': 'Token is invalid'}), 401
                
            return f(response.json(), *args, **kwargs)
        except requests.RequestException:
            return jsonify({'message': 'Service unavailable'}), 503
    return decorated
