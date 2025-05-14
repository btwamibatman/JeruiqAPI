from flask import Flask
import logging
from adapters.web.rest.user_routes import user_blueprint as user_bp
from adapters.web.rest.auth_routes import auth_blueprint as auth_bp  # Assuming auth_routes contains role-related routes
from adapters.web.rest.chat_routes import chat_blueprint as chat_bp  # Add chat routes
from adapters.web.rest.health_check import health_bp as health_bp
from infrastructure.db.session import init_db  # Adjust based on your structure
from infrastructure.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

# Initialize Database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {str(e)}")
    raise

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')  # Assuming auth_routes handles role-related routes
app.register_blueprint(chat_bp, url_prefix='/api')  # Register chat routes
app.register_blueprint(health_bp, url_prefix='/api')

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', port=5002, debug=Config.DEBUG)