from functools import wraps
from flask import jsonify

class Permission:
    """Defines available user permissions."""
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
    def has_permission(role, permission):
        """Checks if a role has the required permission."""
        return permission in Permission.ROLE_PERMISSIONS.get(role, set())

def require_permission(permission):
    """Middleware to enforce role-based access control."""
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            role = current_user.get("role", "user")  # Default role: "user"
            
            if not Permission.has_permission(role, permission):
                return jsonify({"message": "Permission denied"}), 403
            
            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator