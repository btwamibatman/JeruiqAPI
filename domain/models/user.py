from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    """Represents a user in the domain."""
    name: str
    surname: str
    email: str
    password_hash: str # Store the hashed password, not the plain password
    # This should generate the user_id automatically
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: str = field(default="user")