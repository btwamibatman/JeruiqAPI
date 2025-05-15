from pydantic import BaseModel
from datetime import datetime

class ChatSchema(BaseModel):
    id: int
    user_id: int
    message: str
    response: str
    timestamp: datetime