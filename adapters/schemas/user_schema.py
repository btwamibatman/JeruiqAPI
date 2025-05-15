from pydantic import BaseModel, EmailStr, validator, Field
from adapters.auth.password_hasher import PasswordHasher
from core.entities.role import Role
from uuid import UUID
from datetime import datetime
from typing import Optional

# Input schema for user registration
class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone_number: Optional[str] = Field(None, min_length=5)

    @validator('password', pre=True)
    def hash_password(cls, v):
        return PasswordHasher().hash_password(v) if v else v

# Output schema for user responses
class UserResponseSchema(BaseModel):
    user_id: UUID
    name: str
    email: EmailStr
    phone_number: Optional[str]
    role: str
    created_at: datetime
    updated_at: Optional[datetime]

    @validator('role')
    def validate_role(cls, v):
        if not Role.is_valid(v):
            raise ValueError("Invalid role")
        return v

    class Config:
        from_attributes = True  # Allows mapping from ORM models