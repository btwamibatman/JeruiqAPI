from dataclasses import dataclass
from typing import Optional

@dataclass
class SearchFilter:
    rating_min: Optional[float] = None
    price_level: Optional[int] = None
    open_now: Optional[bool] = None
    # Add more fields as needed