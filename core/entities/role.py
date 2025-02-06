class Role:
    USER = "user"
    ADMIN = "admin"
    GUIDE = "guide"

    @staticmethod
    def is_valid(role: str) -> bool:
        return role in {Role.USER, Role.ADMIN, Role.GUIDE}
