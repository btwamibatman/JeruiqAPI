from flask import Blueprint, jsonify
from .middleware import token_required
from models.chat_session import ChatSessionManager

session_bp = Blueprint("session", __name__)

@session_bp.route('/sessions/<session_id>', methods=['DELETE'])
@token_required
def clear_session(current_user, session_id):
    user_id = current_user.get("sub")
    full_session_id = f"{user_id}_{session_id}"

    try:
        ChatSessionManager.clear_session(full_session_id)
        return jsonify({"message": "Session cleared successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to clear session"}), 500
