from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG,)
logger = logging.getLogger(__name__)

# Создаём экземпляр Flask
app = Flask(__name__)
CORS(app)

# Импортируем маршруты и обработчики ошибок
from infrastructure.config import Config
app.config.from_object(Config)
app.config['DEBUG'] = True  # Включаем режим отладки

# Register blueprints
from adapters.web.rest import api_blueprint
from adapters.error_handlers.error_handlers import handle_exception
from presentation.frontend import frontend_bp
from presentation.routes.chat_routes import chat_bp

app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_bp)
app.register_blueprint(chat_bp, url_prefix='/api/chat')
app.register_error_handler(Exception, handle_exception)

# Error handler for 500 errors
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

# Error handler for 400 errors
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400

# Добавляем маршрут для корневого URL
@app.route("/")
@app.route("/getstarted")
def getstarted():
    return render_template("startpage.html")

@app.route('/signuppage')
def signup_page():
    return render_template('signuppage.html')

@app.route('/loginpage')
def login_page():
    return render_template('loginpage.html')

@app.route('/home')
def home_page():
    return render_template('mainpage.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)