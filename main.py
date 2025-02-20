from flask import Flask, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Create the Flask application instance
app = Flask(__name__)

# Load configuration
from infrastructure.config import Config
app.config.from_object(Config)

# Register API blueprint and error handler
from adapters.web.rest import api_blueprint
from adapters.web.error_handlers import handle_exception
app.register_blueprint(api_blueprint)
app.register_error_handler(Exception, handle_exception)

# If you have additional routes (e.g., from the "pages" module), import them.
# This import should register any extra routes on the `app` instance.

# Define a simple home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Jeruiq API!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
