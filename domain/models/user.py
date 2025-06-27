import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from .bookmark import Bookmark

@dataclass
class User:
    """Represents a user in the domain."""
    name: str
    surname: str
    email: str
    password_hash: str # Store the hashed password, not the plain password
    bio: Optional[str] = None
    profile_picture: Optional[str] = None  # URL or path to the profile picture
    # This should generate the user_id automatically
    social_links: Optional[dict] = field(default_factory=dict)  # Store social media links as a dictionary
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    role: str = field(default="user")
    bookmarks: List[Bookmark] = field(default_factory=list)