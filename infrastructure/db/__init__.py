from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from infrastructure.db.base import Base
from infrastructure.db.session import engine
import os

# Загружаем переменные из .env
load_dotenv()

# Читаем URL базы данных из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Проверяем, есть ли переменная, иначе вызываем ошибку
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не задан в .env")

# Создаём подключение к БД
engine = create_engine(DATABASE_URL, echo=True)

# Создаём сессию для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
