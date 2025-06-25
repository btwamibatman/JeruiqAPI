from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class UserQuery:
    raw_text: str
    category: Optional[str] = None
    filters: Optional[Dict[str, str]] = None  # e.g., {"rating": ">4.5"}