from flask import Flask
import logging
from api_gateway.routes.health_check import health_bp
from api_gateway.routes.auth_routes import auth_bp
from api_gateway.routes.user_routes import user_bp
from api_gateway.routes.ai_routes import ai_bp
from presentation.frontend import frontend_bp
from presentation.routes.chat_routes import chat_bp
from adapters.error_handlers.web_error_handlers import register_error_handlers
from dotenv import load_dotenv
import os

load_dotenv()
# Load environment variables

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register Error Handlers
register_error_handlers(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(health_bp)
app.register_blueprint(frontend_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) # Set debug to False in production