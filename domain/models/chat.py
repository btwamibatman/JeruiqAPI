from dataclasses import dataclass
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Optional

@dataclass
class Chat:
    session_id: UUID
    user_id: UUID
    messages: List[dict] = None  # List of {"role": "user" or "ai", "content": str}
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.session_id:
            self.session_id = uuid4()
        if not self.user_id:
            raise ValueError("User ID is required")
        if self.messages is None:
            self.messages = []
        if not isinstance(self.messages, list):
            raise ValueError("Messages must be a list")

    def add_message(self, role: str, content: str) -> None:
        if role not in ["user", "ai"]:
            raise ValueError("Role must be 'user' or 'ai'")
        self.messages.append({"role": role, "content": content})
        self.updated_at = datetime.utcnow()

    def get_last_message(self) -> Optional[dict]:
        return self.messages[-1] if self.messages else None