from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from gemini_integration import get_response
import uuid
import os

# Создаём экземпляр Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# Загружаем конфигурацию
from infrastructure.config import Config
app.config.from_object(Config)

@app.before_request
def before_request():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

# Добавляем маршрут для корневого URL
@app.route("/", methods=["GET"])
def home():
    return render_template("startpage.html")

@app.route("/index", methods=["GET"])
def index():
    # Alias for home page
    return redirect(url_for('home'))

@app.route("/chat", methods=["GET"])
def chat():
    # Pass initial query parameter to the template if it exists
    initial_query = request.args.get('initial_query', '')
    return render_template("chat.html", initial_query=initial_query)

@app.post("/response")
def response():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"message": "No message provided"}), 400
        
        text = data.get("message")
        if not text:
            return jsonify({"message": "Empty message provided"}), 400
        
        ai_response = get_response(text, session.get('user_id'))
        return jsonify({"message": ai_response})
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({"message": "An error occurred processing your request"}), 500
