from flask import Blueprint, request, Response, jsonify
import requests
import os
from .middleware import token_required  # Import authentication middleware

ai_bp = Blueprint('ai', __name__)
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:5003")

@ai_bp.route('/ai/chat', methods=['POST'])
@token_required
def chat(current_user):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        data = request.json
        data['user_id'] = current_user.get('sub')

        response = requests.post(f"{AI_SERVICE_URL}/chat", json=data, headers={"Authorization": f"Bearer {token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "AI service unavailable"}), 503

@ai_bp.route('/ai/sessions/<session_id>', methods=['DELETE'])
@token_required
def clear_chat_session(current_user, session_id):
    try:
        token = request.headers['Authorization'].split(" ")[1]
        response = requests.delete(f"{AI_SERVICE_URL}/sessions/{session_id}", headers={"Authorization": f"Bearer {token}"})
        return Response(response.content, response.status_code, content_type=response.headers['Content-Type'])
    except requests.RequestException:
        return jsonify({"message": "AI service unavailable"}), 503
