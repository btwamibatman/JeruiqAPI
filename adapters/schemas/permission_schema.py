from pydantic import BaseModel

class PermissionSchema(BaseModel):
    id: int
    name: str
    description: str