import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

class Config:
    """Конфигурация проекта"""

    # База данных
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Аутентификация
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @staticmethod
    def validate():
        """Проверка, что все важные переменные установлены"""
        if not Config.DATABASE_URL:
            raise ValueError("DATABASE_URL не найден в .env")
        if not Config.SECRET_KEY:
            raise ValueError("SECRET_KEY не найден в .env")

# Проверяем настройки при загрузке
Config.validate()
