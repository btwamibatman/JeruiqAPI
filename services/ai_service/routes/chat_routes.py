from flask import Blueprint, request, jsonify
from services.ai_service.gemini_ai_model import ChatSession
from uuid import uuid4 as uuid

chat_bp = Blueprint('chat', __name__)
chat_sessions = {}

@chat_bp.route('/api/chat/create_session', methods=['POST'])
def create_session():
    try:
        session_id = str(uuid())
        chat_sessions[session_id] = ChatSession(session_id)
        return jsonify({'session_id': session_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/api/chat/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        message = data.get('message')
        session_id = data.get('session_id')

        if not message or not session_id:
            return jsonify({'error': 'Message and session_id are required'}), 400

        chat_session = chat_sessions.get(session_id)
        if not chat_session:
            chat_session = ChatSession(session_id)
            chat_sessions[session_id] = chat_session

        response = chat_session.send_message(message)
        return jsonify({'response': response}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500