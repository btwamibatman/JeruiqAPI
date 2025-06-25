from dataclasses import dataclass
from typing import Optional

@dataclass
class Place:
    name: str
    lat: float
    lon: float
    category: Optional[str] = None
    rating: Optional[float] = None
    address: Optional[str] = None
    source_id: Optional[str] = None  # e.g., OSM/Photon/Google ID