from core.entities.permission import PermissionModel  # Adjust import
from domain.models.permission import Permission
from infrastructure.db import SessionLocal

class SQLAlchemyPermissionRepository:
    """Репозиторий разрешений через SQLAlchemy"""

    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def create(self, permission: Permission) -> Permission:
        """Создание разрешения в БД"""
        permission_model = PermissionModel(
            id=permission.id,
            name=permission.name,
            description=permission.description
        )
        with self.session_factory() as session:
            session.add(permission_model)
            session.commit()
        return permission

    def get_by_id(self, permission_id: int) -> Permission:
        """Получение разрешения по ID"""
        with self.session_factory() as session:
            permission_model = session.query(PermissionModel).filter_by(id=permission_id).first()
            return permission_model.to_entity() if permission_model else None