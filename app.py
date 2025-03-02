from flask import Flask, jsonify, request, render_template
from adapters.web.rest import api_blueprint
from adapters.web.error_handlers import handle_exception
from infrastructure.config import Config
from routes.frontend import frontend_bp
from uuid import uuid4 as uuid
from services.ai_service.gemini_ai_model import ChatSession
import os

# Создаём экземпляр Flask
app = Flask(__name__)
app.config.from_object(Config)

# Загружаем конфигурацию
from infrastructure.config import Config
app.config.from_object(Config)

# Регистрируем API
app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_bp)
app.register_error_handler(Exception, handle_exception)

chat_sessions = {}

# Добавляем маршрут для корневого URL
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Jeruyiq API!"})

@app.route("/response", methods=["POST"])
def get_ai_response():
    """Handles messages from the frontend and returns AI responses."""
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"message": "Message cannot be empty!"}), 400

    # Generate a unique session ID if not already in use
    session_id = request.cookies.get("session_id") or str(uuid.uuid4())
    if session_id not in chat_sessions:
        chat_sessions[session_id] = ChatSession(session_id)

    chat_session = chat_sessions[session_id]
    ai_response = chat_session.send_message(user_message)

    return jsonify({"message": ai_response})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)