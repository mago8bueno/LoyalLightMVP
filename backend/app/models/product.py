"""
Product/Stock models.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base product model."""
    nombre_producto: str = Field(..., min_length=1, max_length=200)
    precio: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    """Product creation model."""
    stock_inicial: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=5, ge=0)


class ProductUpdate(BaseModel):
    """Product update model."""
    nombre_producto: Optional[str] = Field(None, min_length=1, max_length=200)
    precio: Optional[float] = Field(None, gt=0)
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    imagen_url: Optional[str] = None


class Product(ProductBase):
    """Product model."""
    id: Optional[str] = Field(None, alias="_id")
    stock_actual: int = Field(default=0, ge=0)
    stock_minimo: int = Field(default=5, ge=0)
    imagen_url: Optional[str] = None
    fecha_creacion: datetime
    
    class Config:
        populate_by_name = True


class ProductSalesStats(BaseModel):
    """Product sales statistics."""
    product: Product
    total_vendido: int
    ingresos_totales: float
    ventas_ultimo_mes: int


class StockAlert(BaseModel):
    """Stock alert model."""
    product: Product
    alert_type: str  # "low_stock", "out_of_stock"
    message: str

