from core.entities.permission import Permission
from core.entities.exceptions import UserNotFoundError
class CheckPermissions:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def has_permission(self, user_id: str, permission: str) -> bool:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("Пользователь не найден")
        return Permission.has_permission(user.role, permission)
