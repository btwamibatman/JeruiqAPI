from core.entities.role import RoleModel  # Adjust import
from domain.models.role import Role
from infrastructure.db import SessionLocal

class SQLAlchemyRoleRepository:
    """Репозиторий ролей через SQLAlchemy"""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def create(self, role: Role) -> Role:
        """Создание роли в БД"""
        role_model = RoleModel(
            id=role.id,
            name=role.name,
            description=role.description
        )
        with self.session_factory() as session:
            session.add(role_model)
            session.commit()
        return role

    def get_by_id(self, role_id: int) -> Role:
        """Получение роли по ID"""
        with self.session_factory() as session:
            role_model = session.query(RoleModel).filter_by(id=role_id).first()
            return role_model.to_entity() if role_model else None