import hashlib

class PasswordHasher:
    """Хеширование паролей"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Создаёт хеш пароля"""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Сравнивает пароль с хешем"""
        return hashlib.sha256(password.encode()).hexdigest() == password_hash
