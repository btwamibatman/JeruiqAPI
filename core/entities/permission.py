class Permission:
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MANAGE_USERS = "manage_users"

    ROLE_PERMISSIONS = {
        "user": frozenset([READ]),
        "guider": frozenset([READ, WRITE]),
        "admin": frozenset([READ, WRITE, DELETE, MANAGE_USERS]),
    }

    @staticmethod
    def has_permission(role: str, permission: str) -> bool:
        return permission in Permission.ROLE_PERMISSIONS.get(role, frozenset())