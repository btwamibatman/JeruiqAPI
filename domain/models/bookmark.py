import uuid
from dataclasses import dataclass, field

@dataclass
class Bookmark:
    """Represents a user's bookmarked place."""
    user_id: uuid.UUID # Foreign key linking to the User
    place_id: str      # ID of the bookmarked place (e.g., from Photon or your internal ID)
    name: str          # Name of the bookmarked place
    latitude: float    # Latitude of the bookmarked place
    longitude: float   # Longitude of the bookmarked place

    bookmark_id: uuid.UUID = field(default_factory=uuid.uuid4)
    # Add other relevant fields if needed, e.g., category, description, timestamp