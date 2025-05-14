from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

@dataclass
class User:
    user_id: UUID
    name: str
    email: str
    password_hash: str
    phone_number: Optional[str]
    role: str = "user"
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.user_id:
            self.user_id = uuid4()
        if not self.name or len(self.name) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email address")
        if not self.password_hash:
            raise ValueError("Password hash is required")
        if self.role not in ["user", "admin"]:
            raise ValueError("Invalid role")
        if self.phone_number and len(self.phone_number) < 5:
            raise ValueError("Phone number is too short")

    def update_email(self, new_email: str) -> None:
        if not new_email or "@" not in new_email:
            raise ValueError("Invalid email address")
        self.email = new_email
        self.updated_at = datetime.utcnow()