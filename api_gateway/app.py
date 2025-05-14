from flask import Flask
import logging
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.ai_routes import ai_bp
from routes.health_check import health_bp

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(health_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Disable debug in production
