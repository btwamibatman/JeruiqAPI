from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Загружаем .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в .env")

engine = create_engine(DATABASE_URL)
