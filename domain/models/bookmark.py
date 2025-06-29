import uuid
from dataclasses import dataclass, field

@dataclass
class Bookmark:
    bookmark_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    place_id: str = ""
    name: str = ""
    latitude: str = ""
    longitude: str = ""