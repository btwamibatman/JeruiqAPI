from flask import Blueprint, request, jsonify
from services.ai_service.gemini_ai_model import ChatSession
from uuid import uuid4 as uuid

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/create_session', methods=['POST'])
def create_session():
    session_id = str(uuid())
    # Initialize ChatSession with the session_id
    chat_session = ChatSession(session_id)
    return jsonify({'session_id': session_id}), 201

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    session_id = data.get('session_id')
    message = data.get('message')

    if not session_id or not message:
        return jsonify({'error': 'Missing session_id or message'}), 400

    try:
        # Create a new ChatSession with the existing session_id
        # This will load history from Redis if available
        chat_session = ChatSession(session_id)
        response = chat_session.send_message(message)
        return jsonify({'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500