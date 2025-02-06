🚀 Jeruiq Backend

📌 Project Overview

Jeruiq is a backend service built using Flask and follows the Clean Architecture principles. It provides authentication, user management, and various functionalities for the application.

📂 Project Structure

![image](https://github.com/user-attachments/assets/e7017427-bf6f-4476-b95d-0f7fca6f1855)

(Not all feature from image, has been realized yet)
🔧 Installation & Setup

1️⃣ Clone the repository

git clone https://github.com/your-repo/jeruiq-backend.git
cd jeruiq-backend

2️⃣ Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file in the root directory:

DATABASE_URL=postgresql://user:password@localhost:5432/your_database
SECRET_KEY=your_secret_key

5️⃣ Run Migrations

alembic upgrade head

6️⃣ Start the Application

python main.py

🚀 API Endpoints

🔐 Authentication

POST /auth/register - Register a new user

POST /auth/login - Authenticate and get JWT token

👤 User Management

GET /users/ - Get all users (requires authentication)

🧪 Running Tests

pytest tests/

📌 Technologies Used

Python 3.12

Flask - Web framework

SQLAlchemy - ORM for PostgreSQL

Alembic - Database migrations

JWT - Authentication

Redis - Caching

Celery - Background tasks

📜 License

MIT License © 2025 Jeruiq Team

✅ Now you're all set! 🚀 Need help? Contact the team.
