"""
Dashboard service with business logic.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.dashboard import DashboardMetrics, DashboardData, Alert, ChartData
from ..core.database import get_database


class DashboardService:
    """Dashboard service for business logic."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
    
    async def get_dashboard_metrics(self) -> DashboardMetrics:
        """Get dashboard metrics."""
        # Total counts
        total_clientes = await self.db.clients.count_documents({})
        total_productos = await self.db.products.count_documents({})
        total_compras = await self.db.purchases.count_documents({})
        
        # Total revenue
        revenue_pipeline = [{"$group": {"_id": None, "total": {"$sum": "$total"}}}]
        revenue_result = await self.db.purchases.aggregate(revenue_pipeline).to_list(length=1)
        ingresos_totales = revenue_result[0]["total"] if revenue_result else 0
        
        # Monthly revenue
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_pipeline = [
            {"$match": {"fecha": {"$gte": current_month_start}}},
            {"$group": {"_id": None, "total": {"$sum": "$total"}}}
        ]
        monthly_result = await self.db.purchases.aggregate(monthly_pipeline).to_list(length=1)
        ingresos_mes_actual = monthly_result[0]["total"] if monthly_result else 0
        
        # New clients this month
        new_clients_count = await self.db.clients.count_documents({
            "fecha_registro": {"$gte": current_month_start}
        })
        
        # Products with low stock
        productos_bajo_stock = await self.db.products.count_documents({
            "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}
        })
        
        return DashboardMetrics(
            total_clientes=total_clientes,
            total_productos=total_productos,
            total_compras=total_compras,
            ingresos_totales=ingresos_totales,
            ingresos_mes_actual=ingresos_mes_actual,
            clientes_nuevos_mes=new_clients_count,
            productos_bajo_stock=productos_bajo_stock
        )
    
    async def get_alerts(self) -> List[Alert]:
        """Get system alerts."""
        alerts = []
        
        # High churn risk clients
        high_churn_clients = await self.db.clients.find({"churn_score": {"$gte": 0.7}}).to_list(length=None)
        if high_churn_clients:
            alerts.append(Alert(
                id=str(uuid.uuid4()),
                type="churn",
                title="Clientes con alto riesgo de abandono",
                message=f"{len(high_churn_clients)} clientes tienen alto riesgo de abandono",
                severity="high",
                created_at=datetime.utcnow()
            ))
        
        # Low stock products
        low_stock_products = await self.db.products.find({
            "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}
        }).to_list(length=None)
        
        if low_stock_products:
            out_of_stock = [p for p in low_stock_products if p["stock_actual"] == 0]
            if out_of_stock:
                alerts.append(Alert(
                    id=str(uuid.uuid4()),
                    type="stock",
                    title="Productos sin stock",
                    message=f"{len(out_of_stock)} productos están sin stock",
                    severity="critical",
                    created_at=datetime.utcnow()
                ))
            
            low_stock = [p for p in low_stock_products if p["stock_actual"] > 0]
            if low_stock:
                alerts.append(Alert(
                    id=str(uuid.uuid4()),
                    type="stock",
                    title="Productos con stock bajo",
                    message=f"{len(low_stock)} productos tienen stock bajo",
                    severity="medium",
                    created_at=datetime.utcnow()
                ))
        
        # Sales performance alerts
        last_week = datetime.utcnow() - timedelta(days=7)
        recent_sales = await self.db.purchases.count_documents({"fecha": {"$gte": last_week}})
        
        if recent_sales < 5:  # Threshold for low sales
            alerts.append(Alert(
                id=str(uuid.uuid4()),
                type="sales",
                title="Ventas bajas esta semana",
                message=f"Solo {recent_sales} ventas en los últimos 7 días",
                severity="medium",
                created_at=datetime.utcnow()
            ))
        
        # New client acquisition
        last_month = datetime.utcnow() - timedelta(days=30)
        new_clients = await self.db.clients.count_documents({"fecha_registro": {"$gte": last_month}})
        
        if new_clients == 0:
            alerts.append(Alert(
                id=str(uuid.uuid4()),
                type="general",
                title="Sin nuevos clientes",
                message="No se han registrado nuevos clientes en el último mes",
                severity="medium",
                created_at=datetime.utcnow()
            ))
        
        return alerts
    
    async def get_sales_chart_data(self) -> ChartData:
        """Get sales chart data for the last 7 days."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=6)
        
        # Generate date labels
        labels = []
        current_date = start_date
        while current_date <= end_date:
            labels.append(current_date.strftime("%d/%m"))
            current_date += timedelta(days=1)
        
        # Get daily sales data
        pipeline = [
            {
                "$match": {
                    "fecha": {
                        "$gte": start_date.replace(hour=0, minute=0, second=0, microsecond=0),
                        "$lte": end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$fecha"
                        }
                    },
                    "ventas": {"$sum": 1},
                    "ingresos": {"$sum": "$total"}
                }
            },
            {"$sort": {"_id": 1}}
        ]
        
        daily_data = await self.db.purchases.aggregate(pipeline).to_list(length=None)
        
        # Create data arrays
        sales_data = []
        revenue_data = []
        
        current_date = start_date
        data_dict = {item["_id"]: item for item in daily_data}
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str in data_dict:
                sales_data.append(data_dict[date_str]["ventas"])
                revenue_data.append(data_dict[date_str]["ingresos"])
            else:
                sales_data.append(0)
                revenue_data.append(0)
            current_date += timedelta(days=1)
        
        return ChartData(
            labels=labels,
            datasets=[
                {
                    "label": "Ventas",
                    "data": sales_data,
                    "borderColor": "rgb(59, 130, 246)",
                    "backgroundColor": "rgba(59, 130, 246, 0.1)"
                },
                {
                    "label": "Ingresos",
                    "data": revenue_data,
                    "borderColor": "rgb(16, 185, 129)",
                    "backgroundColor": "rgba(16, 185, 129, 0.1)"
                }
            ]
        )
    
    async def get_complete_dashboard_data(self) -> DashboardData:
        """Get complete dashboard data."""
        from .client_service import client_service
        from .stock_service import stock_service
        
        # Get all dashboard components
        metrics = await self.get_dashboard_metrics()
        alerts = await self.get_alerts()
        top_clients = await client_service.get_top_loyal_clients(limit=5)
        churn_clients = await client_service.get_churn_risk_clients(limit=5)
        stock_alerts = await stock_service.get_stock_alerts()
        sales_chart = await self.get_sales_chart_data()
        
        return DashboardData(
            metrics=metrics,
            alerts=alerts,
            top_clients=[{"client": client, "ranking": i+1, "loyalty_score": 1-client.churn_score} 
                        for i, client in enumerate(top_clients)],
            churn_clients=[{"client": analysis.client, "churn_risk": analysis.churn_risk, 
                           "churn_score": analysis.client.churn_score} 
                          for analysis in churn_clients],
            stock_alerts=stock_alerts,
            sales_chart=sales_chart
        )


# Global service instance
dashboard_service = DashboardService()

