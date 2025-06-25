from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.db.models import User as DBUser # Import SQLAlchemy model
from domain.models.user import User as DomainUser # Import Domain model
from domain.exceptions import DomainException # Import DomainException if used in _to_domain_user

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def _to_domain_user(self, db_user: Optional[DBUser]) -> Optional[DomainUser]:
        """Converts a SQLAlchemy DBUser model to a Domain User model."""
        if db_user is None:
            return None
        # Ensure all fields expected by the DomainUser dataclass are mapped
        return DomainUser(
            user_id=db_user.user_id,
            name=db_user.name,
            surname=db_user.surname,
            email=db_user.email,
            password_hash=db_user.password_hash,
            role=db_user.role
        )

    def _to_db_user(self, domain_user: DomainUser) -> DBUser:
        """Converts a Domain User model to a SQLAlchemy DBUser model."""
        # Ensure all fields expected by the DBUser model are mapped
        db_user = DBUser(
            user_id=domain_user.user_id, # This is where the domain ID is transferred
            name=domain_user.name,
            surname=domain_user.surname,
            email=domain_user.email,
            password_hash=domain_user.password_hash,
            role=domain_user.role
        )
        print(f"[_to_db_user] Domain User ID: {domain_user.user_id}") # Debug print
        print(f"[_to_db_user] DBUser ID after mapping: {db_user.user_id}") # Debug print
        return db_user

    def get_by_id(self, user_id: str) -> Optional[DomainUser]:
        """Get a user by their ID."""
        db_user = self.db_session.query(DBUser).filter(DBUser.user_id == user_id).first()
        return self._to_domain_user(db_user)

    def get_by_email(self, email: str) -> Optional[DomainUser]:
        """Get a user by their email address."""
        db_user = self.db_session.query(DBUser).filter(DBUser.email == email).first()
        return self._to_domain_user(db_user)

    def create(self, user: DomainUser) -> DomainUser:
        """Create a new user from a DomainUser model."""
        print(f"[UserRepository.create] Domain User object received: {user}") # Debug print
        print(f"[UserRepository.create] Domain User ID before mapping: {user.user_id}") # Debug print

        db_user = self._to_db_user(user)

        print(f"[UserRepository.create] DBUser object before add: {db_user}") # Debug print
        print(f"[UserRepository.create] DBUser ID before add: {db_user.user_id}") # Debug print

        self.db_session.add(db_user)

        print("[UserRepository.create] DBUser added to session. Committing...") # Debug print
        self.db_session.commit()
        print("[UserRepository.create] Commit successful. Refreshing...") # Debug print

        self.db_session.refresh(db_user) # Refresh to get the generated ID (though it should already have one)
        print(f"[UserRepository.create] DBUser ID after refresh: {db_user.user_id}") # Debug print

        return self._to_domain_user(db_user) # Return the created DomainUser with ID

# Note: The create_user_repository factory function is likely in infrastructure/db/db.py
# It should provide a session to the UserRepository constructor.