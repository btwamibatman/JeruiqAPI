from core.entities.role import Role

class AssignRole:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def assign(self, user_id: str, new_role: str):
        """Назначает новую роль пользователю"""
        if not Role.is_valid(new_role):
            raise ValueError("Недопустимая роль")

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("Пользователь не найден")

        user.role = new_role
        self.user_repository.save(user)

        return user
