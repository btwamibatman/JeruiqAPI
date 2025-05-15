from dotenv import load_dotenv
import os

class Config:
    DEBUG = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
    AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")
    REDIS_URL = os.getenv("REDIS_URL")

    @staticmethod
    def validate():
        required_vars = [
            ("DATABASE_URL", Config.DATABASE_URL),
            ("SECRET_KEY", Config.SECRET_KEY),
            ("REDIS_URL", Config.REDIS_URL),
        ]
        for var_name, var_value in required_vars:
            if not var_value:
                raise ValueError(f"{var_name} not found in .env")

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:5001")
    USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://localhost:5002")
    AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://localhost:5003")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

class TestingConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Select config based on environment
env = os.getenv("FLASK_ENV", "development").lower()
config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
ActiveConfig = config_map.get(env, DevelopmentConfig)
ActiveConfig.validate()