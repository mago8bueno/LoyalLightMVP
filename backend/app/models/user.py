"""
User models.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base user model."""
    username: str = Field(..., min_length=3, max_length=50)
    role: str = Field(..., pattern="^(admin|client)$")


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login model."""
    username: str
    password: str


class User(UserBase):
    """User model."""
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime
    
    class Config:
        populate_by_name = True


class Token(BaseModel):
    """Token model."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model."""
    username: Optional[str] = None

