from flask import Blueprint, request, jsonify
from domain.services.ai_service.gemini_ai_model import ChatSession
import logging
import uuid

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)
chat_sessions = {}

@chat_bp.route('/create_session', methods=['POST'])
def create_session():
    try:
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Initialize a new chat session
        chat_sessions[session_id] = ChatSession(session_id)
        
        logger.debug(f"Created new session: {session_id}")
        return jsonify({'session_id': session_id}), 201
        
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        message = data.get('message')
        session_id = data.get('session_id')

        logger.debug(f"Received message: {message} for session: {session_id}")

        if not message or not session_id:
            logger.error("Missing message or session_id")
            return jsonify({'error': 'Message and session_id are required'}), 400

        chat_session = chat_sessions.get(session_id)
        if not chat_session:
            logger.info(f"Creating new session for ID: {session_id}")
            chat_session = ChatSession(session_id)
            chat_sessions[session_id] = chat_session

        try:
            response = chat_session.send_message(message)
            logger.debug(f"AI Response: {response}")
            return jsonify({'response': response}), 200
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return jsonify({'error': f"AI error: {str(e)}"}), 500

    except Exception as e:
        logger.exception("Error in send_message endpoint")
        return jsonify({'error': str(e)}), 500