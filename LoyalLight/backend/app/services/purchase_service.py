"""
Purchase service with business logic.
"""
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.purchase import Purchase, PurchaseCreate, PurchaseUpdate, PurchaseWithClient
from ..core.database import get_database


class PurchaseService:
    """Purchase service for business logic."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
    
    async def create_purchase(self, purchase_data: PurchaseCreate) -> Purchase:
        """Create a new purchase."""
        # Verify client exists
        client = await self.db.clients.find_one({"_id": purchase_data.cliente_id})
        if not client:
            raise ValueError("Client not found")
        
        # Calculate total
        total = purchase_data.cantidad * purchase_data.precio_unitario
        
        purchase_dict = purchase_data.dict()
        purchase_dict.update({
            "_id": str(uuid.uuid4()),
            "total": total
        })
        
        await self.db.purchases.insert_one(purchase_dict)
        
        # Update client metrics
        from .client_service import client_service
        await client_service.update_client_metrics(purchase_data.cliente_id)
        
        # Update product stock if exists
        await self._update_product_stock(purchase_data.producto_comprado, purchase_data.cantidad)
        
        return Purchase(**purchase_dict)
    
    async def get_purchase(self, purchase_id: str) -> Optional[Purchase]:
        """Get purchase by ID."""
        purchase = await self.db.purchases.find_one({"_id": purchase_id})
        return Purchase(**purchase) if purchase else None
    
    async def get_purchases(self, skip: int = 0, limit: int = 100) -> List[PurchaseWithClient]:
        """Get list of purchases with client information."""
        pipeline = [
            {
                "$lookup": {
                    "from": "clients",
                    "localField": "cliente_id",
                    "foreignField": "_id",
                    "as": "client_info"
                }
            },
            {
                "$addFields": {
                    "cliente_nombre": {"$arrayElemAt": ["$client_info.nombre", 0]},
                    "cliente_apellido": {"$arrayElemAt": ["$client_info.apellido", 0]}
                }
            },
            {"$project": {"client_info": 0}},
            {"$sort": {"fecha": -1}},
            {"$skip": skip},
            {"$limit": limit}
        ]
        
        cursor = self.db.purchases.aggregate(pipeline)
        purchases = await cursor.to_list(length=limit)
        return [PurchaseWithClient(**purchase) for purchase in purchases]
    
    async def update_purchase(self, purchase_id: str, purchase_data: PurchaseUpdate) -> Optional[Purchase]:
        """Update purchase."""
        update_data = {k: v for k, v in purchase_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_purchase(purchase_id)
        
        # Recalculate total if quantity or price changed
        if "cantidad" in update_data or "precio_unitario" in update_data:
            current_purchase = await self.get_purchase(purchase_id)
            if not current_purchase:
                return None
            
            cantidad = update_data.get("cantidad", current_purchase.cantidad)
            precio_unitario = update_data.get("precio_unitario", current_purchase.precio_unitario)
            update_data["total"] = cantidad * precio_unitario
        
        result = await self.db.purchases.update_one(
            {"_id": purchase_id},
            {"$set": update_data}
        )
        
        if result.modified_count:
            # Update client metrics if client changed
            if "cliente_id" in update_data:
                from .client_service import client_service
                await client_service.update_client_metrics(update_data["cliente_id"])
            
            return await self.get_purchase(purchase_id)
        return None
    
    async def delete_purchase(self, purchase_id: str) -> bool:
        """Delete purchase."""
        purchase = await self.get_purchase(purchase_id)
        if not purchase:
            return False
        
        result = await self.db.purchases.delete_one({"_id": purchase_id})
        
        if result.deleted_count:
            # Update client metrics
            from .client_service import client_service
            await client_service.update_client_metrics(purchase.cliente_id)
            return True
        
        return False
    
    async def get_purchases_by_client(self, client_id: str) -> List[Purchase]:
        """Get purchases by client ID."""
        cursor = self.db.purchases.find({"cliente_id": client_id}).sort("fecha", -1)
        purchases = await cursor.to_list(length=None)
        return [Purchase(**purchase) for purchase in purchases]
    
    async def get_recent_purchases(self, days: int = 30) -> List[PurchaseWithClient]:
        """Get recent purchases."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        pipeline = [
            {"$match": {"fecha": {"$gte": start_date}}},
            {
                "$lookup": {
                    "from": "clients",
                    "localField": "cliente_id",
                    "foreignField": "_id",
                    "as": "client_info"
                }
            },
            {
                "$addFields": {
                    "cliente_nombre": {"$arrayElemAt": ["$client_info.nombre", 0]},
                    "cliente_apellido": {"$arrayElemAt": ["$client_info.apellido", 0]}
                }
            },
            {"$project": {"client_info": 0}},
            {"$sort": {"fecha": -1}}
        ]
        
        cursor = self.db.purchases.aggregate(pipeline)
        purchases = await cursor.to_list(length=None)
        return [PurchaseWithClient(**purchase) for purchase in purchases]
    
    async def get_sales_analytics(self) -> Dict[str, Any]:
        """Get sales analytics data."""
        # Total sales
        total_sales = await self.db.purchases.count_documents({})
        
        # Total revenue
        pipeline = [{"$group": {"_id": None, "total_revenue": {"$sum": "$total"}}}]
        revenue_result = await self.db.purchases.aggregate(pipeline).to_list(length=1)
        total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
        
        # Monthly revenue
        current_month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_pipeline = [
            {"$match": {"fecha": {"$gte": current_month_start}}},
            {"$group": {"_id": None, "monthly_revenue": {"$sum": "$total"}}}
        ]
        monthly_result = await self.db.purchases.aggregate(monthly_pipeline).to_list(length=1)
        monthly_revenue = monthly_result[0]["monthly_revenue"] if monthly_result else 0
        
        # Top products
        top_products_pipeline = [
            {
                "$group": {
                    "_id": "$producto_comprado",
                    "total_vendido": {"$sum": "$cantidad"},
                    "ingresos": {"$sum": "$total"}
                }
            },
            {"$sort": {"total_vendido": -1}},
            {"$limit": 10}
        ]
        top_products = await self.db.purchases.aggregate(top_products_pipeline).to_list(length=10)
        
        return {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
            "monthly_revenue": monthly_revenue,
            "top_products": top_products
        }
    
    async def _update_product_stock(self, product_name: str, quantity_sold: int):
        """Update product stock after purchase."""
        await self.db.products.update_one(
            {"nombre_producto": product_name},
            {"$inc": {"stock_actual": -quantity_sold}}
        )


# Global service instance
purchase_service = PurchaseService()

