from flask import Blueprint, request, jsonify
from domain.services.chat_service.chat_service import ChatService
from domain.models.chat import Chat
from uuid import UUID
from adapters.auth.jwt_auth import token_required  # Assuming this decorator exists

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/api/chat/create_session', methods=['POST'])
@token_required
def create_session(current_user):
    user_id = current_user.user_id  # Extracted from token by @token_required
    chat = ChatService().start_chat(user_id)
    return jsonify({"session_id": str(chat.session_id)})

@chat_bp.route('/api/chat/send_message', methods=['POST'])
@token_required
def send_message(current_user):
    data = request.get_json()
    message = data.get('message')
    session_id = data.get('session_id')
    if not message or not session_id:
        return jsonify({"error": "Missing message or session_id"}), 400
    chat = Chat(session_id=UUID(session_id), user_id=current_user.user_id)
    response = ChatService().send_message(chat, message)
    return jsonify({"response": response, "session_id": str(session_id)})