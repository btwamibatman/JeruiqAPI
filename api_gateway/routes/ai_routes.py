from flask import Blueprint, request, Response, jsonify
from functools import wraps
import requests
import os
from adapters.schemas.chat_schema import ChatSchema

ai_bp = Blueprint('ai', __name__)
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:5003")

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
            response = requests.post(f"{AI_SERVICE_URL}/auth/validate-token", headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                return jsonify({'message': 'Token is invalid'}), 401
            request.token = token  # Store token in request context
            return f(response.json(), *args, **kwargs)
        except requests.RequestException:
            return jsonify({'message': 'Service unavailable'}), 503
    return decorated

@ai_bp.route('/ai/chat', methods=['POST'])
def chat(current_user):
    try:
        data = request.json
        ChatSchema(**data)  # Validate input
        data['user_id'] = current_user.get('sub')
        response = requests.post(f"{AI_SERVICE_URL}/chat", json=data, headers={"Authorization": f"Bearer {request.token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException:
        return jsonify({"message": "AI service unavailable"}), 503

@ai_bp.route('/ai/sessions/<session_id>', methods=['DELETE'])
def clear_chat_session(current_user, session_id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        response = requests.delete(f"{AI_SERVICE_URL}/sessions/{session_id}", headers={"Authorization": f"Bearer {token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "AI service unavailable"}), 503
