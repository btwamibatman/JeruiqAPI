from flask import Flask, jsonify
from adapters.web.rest import api_blueprint
from adapters.web.error_handlers import handle_exception
import os

# Создаём экземпляр Flask
app = Flask(__name__)

# Загружаем конфигурацию
from infrastructure.config import Config
app.config.from_object(Config)

# Регистрируем API
app.register_blueprint(api_blueprint)
app.register_error_handler(Exception, handle_exception)

# Добавляем маршрут для корневого URL
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Jeruiq API!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
