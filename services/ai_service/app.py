from flask import Flask
import logging
from routes.chat_routes import chat_bp
from routes.session_routes import session_bp
from routes.health_check import health_bp
from infrastructure.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register Blueprints
app.register_blueprint(chat_bp)
app.register_blueprint(session_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=Config.DEBUG)