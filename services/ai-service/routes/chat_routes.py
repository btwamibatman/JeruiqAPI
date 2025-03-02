from flask import Blueprint, request, jsonify
import uuid
from .middleware import token_required
from models.chat_session import get_response

chat_bp = Blueprint("chat", __name__)

@chat_bp.route('/chat', methods=['POST'])
@token_required
def chat(current_user):
    data = request.json
    user_message = data.get("message")
    session_id = data.get("session_id")
    user_id = current_user.get("sub")  

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if not session_id:
        session_id = f"{user_id}_{str(uuid.uuid4())}"

    try:
        full_session_id = f"{user_id}_{session_id}"
        ai_response = get_response(user_message, full_session_id)
        
        return jsonify({"response": ai_response, "session_id": session_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to process request"}), 500
