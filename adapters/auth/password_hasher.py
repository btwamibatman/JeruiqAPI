import bcrypt
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PasswordHasher:

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширование пароля с bcrypt"""
        logger.debug(f"Hashing password: {password}")
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        logger.debug(f"Hashed password: {hashed_password}, length: {len(hashed_password)}")
        return hashed_password

    @staticmethod
    def verify_password(password, password_hash) -> bool:
        """Проверка пароля"""
        try:
            return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False