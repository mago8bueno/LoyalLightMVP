"""
Client models.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class ClientBase(BaseModel):
    """Base client model."""
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    correo_electronico: EmailStr


class ClientCreate(ClientBase):
    """Client creation model."""
    pass


class ClientUpdate(BaseModel):
    """Client update model."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    correo_electronico: Optional[EmailStr] = None


class Client(ClientBase):
    """Client model."""
    id: Optional[str] = Field(None, alias="_id")
    fecha_registro: datetime
    churn_score: float = Field(default=0.0, ge=0.0, le=1.0)
    total_compras: int = Field(default=0, ge=0)
    valor_total: float = Field(default=0.0, ge=0.0)
    
    class Config:
        populate_by_name = True


class ClientChurnAnalysis(BaseModel):
    """Client churn analysis model."""
    client: Client
    churn_risk: str  # "low", "medium", "high"
    suggestions: Optional[str] = None

