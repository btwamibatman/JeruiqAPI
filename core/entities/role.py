class Role:
    USER = "user"
    ADMIN = "admin"
    GUIDER = "guider"

    @staticmethod
    def is_valid(role: str) -> bool:
        return role in {Role.USER, Role.ADMIN, Role.GUIDER}
