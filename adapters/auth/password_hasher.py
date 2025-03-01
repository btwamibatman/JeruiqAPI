import bcrypt

class PasswordHasher:

    @staticmethod
    def hash_password(password) -> str:
        """Хеширование пароля с bcrypt"""
        print(password)
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print("THIS IS HASH:", hashed_password)
        print("THIS IS len(HASH):", len(hashed_password))
        return hashed_password


    @staticmethod
    def verify_password(password, password_hash) -> bool:
        """Проверка пароля"""
        # if isinstance(password_hash, str):
        #     password_hash = password_hash.encode()  # Приводим строку к байтам
        # print("THIS IS HASH:", bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8")))
        # return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
        userBytes = password.encode('utf-8') 

        print(password_hash)
        print(password)
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))