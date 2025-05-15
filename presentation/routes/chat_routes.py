from flask import Blueprint, request, jsonify
from domain.services.ai_service.gemini_ai_model import ChatSession
from api_gateway.middleware import token_required
from adapters.schemas.chat_schema import ChatSchema
from datetime import datetime, timedelta
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)
chat_sessions = {}

def cleanup_sessions():
    threshold = datetime.now() - timedelta(minutes=30)
    chat_sessions.clear()

@chat_bp.route('/create_session', methods=['POST'])
@token_required
def create_session(current_user):
    try:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = ChatSession(session_id, user_id=current_user.get("user_id"))
        logger.debug(f"Created new session: {session_id} for user: {current_user.get('user_id')}")
        cleanup_sessions()
        return jsonify({'session_id': session_id}), 201
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/send_message', methods=['POST'])
@token_required
def send_message(current_user):
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        validated_data = ChatSchema(**data)  # Validate input
        message = validated_data.message
        session_id = validated_data.session_id

        logger.debug(f"Received message: {message} for session: {session_id}")

        chat_session = chat_sessions.get(session_id)
        if not chat_session:
            logger.info(f"Creating new session for ID: {session_id}")
            chat_session = ChatSession(session_id, user_id=current_user.get("user_id"))
            chat_sessions[session_id] = chat_session

        response = chat_session.send_message(message)
        logger.debug(f"AI Response: {response}")
        return jsonify({'response': response}), 200
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.exception("Error in send_message endpoint")
        return jsonify({'error': str(e)}), 500