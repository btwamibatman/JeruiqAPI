# Jeruyiq

Jeruyiq is a backend application built with Flask, designed to provide services related to exploring places and interacting with AI, specifically focused on Kazakhstan. It includes features for user authentication, searching for locations using the Photon API, interacting with the Gemini AI model, and managing user data.

## Features

*   **User Authentication:** Register and log in users using JWT tokens.
*   **Location Search:** Search for places within Kazakhstan using the Photon API.
*   **AI Interaction:** Integrate with the Gemini API for conversational AI features.
*   **Data Persistence:** Store user information and potentially other data using SQLAlchemy and SQLite.
*   **Modular Design:** Structured with layers (infrastructure, domain, application, adapters) following principles like Dependency Injection.

## Technologies Used

*   **Backend:** Flask, Python
*   **Database:** SQLite
*   **ORM:** SQLAlchemy
*   **Database Migrations:** Alembic
*   **Authentication:** JWT (JSON Web Tokens), Bcrypt for password hashing
*   **External APIs:** Photon (for geocoding/search), Google Gemini (for AI)
*   **Frontend (Integrated):** HTML, CSS (Tailwind CSS), JavaScript, Leaflet (for mapping)

## Setup

Follow these steps to get the project up and running on your local machine.

### Prerequisites

*   Python 3.8+
*   pip (Python package installer)
*   Git

### 1. Clone the Repository

```bash
git clone https://github.com/btwamibatman/JeruiqAPI.git
cd JeruyiqAPI
```

### 2. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```powershell
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using pip.

```powershell
pip install -r requirements.txt
```

### 4. Configuration

The application uses environment variables for configuration. Create a .env file in the project root directory.

```
# .env file
DEBUG=True # Set to False for production
SQLALCHEMY_DATABASE_URL=sqlite:///./jeruyiq.db # Database URL (SQLite example)

# Authentication
SECRET_KEY=your_flask_secret_key # Replace with a strong, random key
JWT_SECRET_KEY=your_jwt_secret_key # Replace with a strong, random key
JWT_EXPIRATION_MINUTES=60 # Token expiration time in minutes

# External API Keys
GEMINI_API_KEY=your_gemini_api_key # Get from Google AI Studio
MAPBOX_API_KEY=your_mapbox_api_key # Needed for some map features if not using Stadia

# Logging
LOG_LEVEL=INFO # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Replace placeholder values with your actual keys and desired settings.

### 5. Database Setup and Migrations

```powershell
# Initialize Alembic (if not already done)
# alembic init alembic # Only run this once if setting up from scratch

# Review the generated migration script (if any)
# alembic revision -m "create users table" # Example: if you change models

# Apply migrations
alembic upgrade head
```

If you encounter table already exists errors during alembic upgrade head, ensure you have deleted the jeruyiq.db file before running the command.

### 6. Run the Application

Start the Flask development server.

```powershell
python app.py
```

The application should now be running at http://127.0.0.1:5000/ (or the port specified in your .env or code).

## Project Structure

```
JeruyiqAPI/
├── alembic/                 # Alembic migration scripts
├── application/             # Application layer (Use Cases, Services)
│   ├── services/
│   └── use_cases/
├── adapters/                # Adapters layer (Web/REST, CLI, etc.)
│   └── web/
│       ├── rest/            # Flask Blueprints
│       └── error_handlers.py
├── domain/                  # Domain layer (Models, Services, Exceptions, Repositories Interfaces)
│   ├── models/
│   ├── services/
│   ├── exceptions.py
│   └── repositories.py
├── infrastructure/          # Infrastructure layer (DB, External Clients, Config)
│   ├── db/                  # Database setup, models, repositories implementations
│   ├── external/            # External API clients
│   └── config.py            # Configuration loading
├── routes/                  # Frontend routes (if serving HTML)
├── static/                  # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── geojson/             # GeoJSON data for map borders
├── templates/               # HTML templates
├── .env                     # Environment variables (create this file)
├── .gitignore               # Specifies intentionally untracked files
├── alembic.ini              # Alembic configuration
├── app.py                   # Flask application entry point
├── requirements.txt         # Project dependencies
└── README.md                # Project README
```

## License

This project is licensed under the MIT License - see the LICENSE file for details (if you have one).