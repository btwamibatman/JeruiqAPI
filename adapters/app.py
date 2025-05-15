# adapters/app.py
from flask import Flask
from infrastructure.config import ActiveConfig  # Updated from /infrastructure
from adapters.routes.chat_routes import chat_bp
from adapters.routes.session_routes import session_bp
from adapters.routes.health_check import health_bp
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config.from_object(ActiveConfig)
CORS(app)

logging.basicBasicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.register_blueprint(chat_bp)
app.register_blueprint(session_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=ActiveConfig.DEBUG)