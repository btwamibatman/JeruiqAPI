from dataclasses import dataclass, field
import uuid

@dataclass
class Trip:
    trip_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    title: str = ""
    start_date: str = ""
    image_url: str = ""
    points: int = 0