import os
from infrastructure.config import Config
from app_factory import create_app # Import the factory function

# Create the Flask application using the factory function
app = create_app(config_object=Config)

# The rest of the file remains the same, just running the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=Config.DEBUG)