class Permission:
    """права доступа пользователей в системе"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"
    
    ROLE_PERMISSIONS = {
        "user": {READ},
        "guider": {READ, WRITE},
        "admin": {READ, WRITE, DELETE, MANAGE_USERS},
    }

    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        """Проверяет, есть ли у роли определенное право доступа"""
        return permission in Permission.ROLE_PERMISSIONS.get(role, set())
