import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Config:
    """Конфигурация проекта"""

    # Отладка
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Аутентификация
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")
    AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:5003")
    
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

    @staticmethod
    def validate():
        """Проверка, что все важные переменные установлены"""
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL не найден в .env")
        if not Config.SECRET_KEY:
            raise ValueError("SECRET_KEY не найден в .env")

# Проверяем настройки при загрузке
Config.validate()
