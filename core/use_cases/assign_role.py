from core.entities.role import Role
from core.entities.exceptions import UserNotFoundError

def assign(self, user_id: str, new_role: str):
    if not Role.is_valid(new_role):
        raise ValueError("Недопустимая роль")

    user = self.user_repository.get_by_id(user_id)
    if not user:
        raise UserNotFoundError("Пользователь не найден")

    user.role = new_role
    self.user_repository.save(user)
    return user
