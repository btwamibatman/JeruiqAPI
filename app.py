from flask import Flask, jsonify, request, render_template
import logging
from services.ai_service.gemini_ai_model import ChatSession
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG,)

# Создаём экземпляр Flask
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Импортируем маршруты и обработчики ошибок
# Загружаем конфигурацию
from infrastructure.config import Config
app.config.from_object(Config)

app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_bp)
app.register_error_handler(Exception, handle_exception)

    return jsonify({'error': 'Internal Server Error'}), 500

# Error handler for 400 errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

# Добавляем маршрут для корневого URL
@app.route("/")
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Jeruyiq API!"})

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