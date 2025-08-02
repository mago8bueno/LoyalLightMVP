"""
Status Check data models.

This module defines Pydantic models for status check operations,
including request/response schemas and validation logic.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StatusCheckBase(BaseModel):
    """
    Base status check model with common fields.
    
    Contains fields that are shared between different status check schemas.
    """
    
    client_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the client for status check",
        example="Acme Corporation"
    )


class StatusCheckCreate(StatusCheckBase):
    """
    Status check creation schema.
    
    Used for creating new status check records. Contains only the fields
    that can be provided by the client during creation.
    """
    
    pass


class StatusCheck(StatusCheckBase):
    """
    Complete status check model.
    
    Represents a full status check record with all fields including
    auto-generated ones like ID and timestamp.
    """
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the status check",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp when the status check was created",
        example="2025-03-15T10:30:00Z"
    )
    
    class Config:
        """Pydantic model configuration."""
        
        # Allow model to be used with ORM-like objects
        from_attributes = True
        
        # JSON schema customization
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "client_name": "Acme Corporation",
                "timestamp": "2025-03-15T10:30:00Z"
            }
        }


class StatusCheckResponse(StatusCheck):
    """
    Status check API response model.
    
    Used for API responses. Currently identical to StatusCheck but kept
    separate for future extensibility (e.g., adding computed fields).
    """
    
    pass