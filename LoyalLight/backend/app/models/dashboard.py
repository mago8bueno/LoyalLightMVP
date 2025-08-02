"""
Dashboard models.
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .client import Client
from .product import Product, StockAlert


class DashboardMetrics(BaseModel):
    """Dashboard metrics model."""
    total_clientes: int
    total_productos: int
    total_compras: int
    ingresos_totales: float
    ingresos_mes_actual: float
    clientes_nuevos_mes: int
    productos_bajo_stock: int


class TopClient(BaseModel):
    """Top client model."""
    client: Client
    ranking: int
    loyalty_score: float


class ChurnClient(BaseModel):
    """Client with churn risk."""
    client: Client
    churn_risk: str  # "high", "medium", "low"
    churn_score: float
    suggested_actions: Optional[str] = None


class Alert(BaseModel):
    """Alert model."""
    id: str
    type: str  # "churn", "stock", "sales", "general"
    title: str
    message: str
    severity: str  # "low", "medium", "high", "critical"
    created_at: datetime
    is_read: bool = False


class ChartData(BaseModel):
    """Chart data model."""
    labels: List[str]
    datasets: List[Dict[str, Any]]


class DashboardData(BaseModel):
    """Complete dashboard data."""
    metrics: DashboardMetrics
    alerts: List[Alert]
    top_clients: List[TopClient]
    churn_clients: List[ChurnClient]
    stock_alerts: List[StockAlert]
    sales_chart: ChartData
    ai_insights: Optional[str] = None

