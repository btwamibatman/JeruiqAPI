from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from adapters.web.rest import api_blueprint
from adapters.web.error_handlers import handle_exception
from infrastructure.config import Config
from routes.frontend import frontend_bp
from routes.chat_routes import chat_bp
import os

# Создаём экземпляр Flask
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Загружаем конфигурацию
from infrastructure.config import Config
app.config.from_object(Config)

# Регистрируем API
app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_bp)
app.register_blueprint(chat_bp)
app.register_error_handler(Exception, handle_exception)

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
    app.run(host="0.0.0.0", port=5000, debug=Config.DEBUG)