from flask import Flask
import logging
from routes.user_routes import user_bp
from routes.role_routes import role_bp
from routes.health_check import health_bp
from models import init_db
from infrastructure.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Database
init_db()

# Register Blueprints
app.register_blueprint(user_bp)
app.register_blueprint(role_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=Config.DEBUG)