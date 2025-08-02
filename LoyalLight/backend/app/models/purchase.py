"""
Purchase models.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PurchaseBase(BaseModel):
    """Base purchase model."""
    producto_comprado: str = Field(..., min_length=1, max_length=200)
    cliente_id: str = Field(..., min_length=1)
    cantidad: int = Field(..., gt=0)
    fecha: datetime


class PurchaseCreate(PurchaseBase):
    """Purchase creation model."""
    precio_unitario: float = Field(..., gt=0)


class PurchaseUpdate(BaseModel):
    """Purchase update model."""
    producto_comprado: Optional[str] = Field(None, min_length=1, max_length=200)
    cliente_id: Optional[str] = None
    cantidad: Optional[int] = Field(None, gt=0)
    fecha: Optional[datetime] = None
    precio_unitario: Optional[float] = Field(None, gt=0)


class Purchase(PurchaseBase):
    """Purchase model."""
    id: Optional[str] = Field(None, alias="_id")
    precio_unitario: float = Field(..., gt=0)
    total: float = Field(..., gt=0)
    
    class Config:
        populate_by_name = True


class PurchaseWithClient(Purchase):
    """Purchase model with client information."""
    cliente_nombre: Optional[str] = None
    cliente_apellido: Optional[str] = None

