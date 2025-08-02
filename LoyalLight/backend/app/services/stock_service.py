"""
Stock/Product service with business logic.
"""
import uuid
import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.product import Product, ProductCreate, ProductUpdate, ProductSalesStats, StockAlert
from ..core.database import get_database


class StockService:
    """Stock/Product service for business logic."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
    
    async def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        # Check if product name already exists
        existing_product = await self.db.products.find_one(
            {"nombre_producto": product_data.nombre_producto}
        )
        if existing_product:
            raise ValueError("Product name already exists")
        
        product_dict = product_data.dict()
        product_dict.update({
            "_id": str(uuid.uuid4()),
            "stock_actual": product_dict.pop("stock_inicial", 0),
            "fecha_creacion": datetime.utcnow(),
            "imagen_url": None
        })
        
        await self.db.products.insert_one(product_dict)
        return Product(**product_dict)
    
    async def get_product(self, product_id: str) -> Optional[Product]:
        """Get product by ID."""
        product = await self.db.products.find_one({"_id": product_id})
        return Product(**product) if product else None
    
    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get list of products."""
        cursor = self.db.products.find().skip(skip).limit(limit)
        products = await cursor.to_list(length=limit)
        return [Product(**product) for product in products]
    
    async def update_product(self, product_id: str, product_data: ProductUpdate) -> Optional[Product]:
        """Update product."""
        update_data = {k: v for k, v in product_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_product(product_id)
        
        # Check name uniqueness if updating name
        if "nombre_producto" in update_data:
            existing_product = await self.db.products.find_one({
                "nombre_producto": update_data["nombre_producto"],
                "_id": {"$ne": product_id}
            })
            if existing_product:
                raise ValueError("Product name already exists")
        
        result = await self.db.products.update_one(
            {"_id": product_id},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        """Delete product."""
        result = await self.db.products.delete_one({"_id": product_id})
        return result.deleted_count > 0
    
    async def upload_product_image(self, product_id: str, image_path: str) -> Optional[Product]:
        """Update product image URL."""
        result = await self.db.products.update_one(
            {"_id": product_id},
            {"$set": {"imagen_url": image_path}}
        )
        
        if result.modified_count:
            return await self.get_product(product_id)
        return None
    
    async def get_low_stock_products(self) -> List[Product]:
        """Get products with low stock."""
        cursor = self.db.products.find({
            "$expr": {"$lte": ["$stock_actual", "$stock_minimo"]}
        })
        products = await cursor.to_list(length=None)
        return [Product(**product) for product in products]
    
    async def get_stock_alerts(self) -> List[StockAlert]:
        """Get stock alerts."""
        alerts = []
        
        # Low stock alerts
        low_stock_products = await self.get_low_stock_products()
        for product in low_stock_products:
            if product.stock_actual == 0:
                alert_type = "out_of_stock"
                message = f"Producto '{product.nombre_producto}' sin stock"
            else:
                alert_type = "low_stock"
                message = f"Producto '{product.nombre_producto}' con stock bajo ({product.stock_actual} unidades)"
            
            alerts.append(StockAlert(
                product=product,
                alert_type=alert_type,
                message=message
            ))
        
        return alerts
    
    async def get_product_sales_stats(self, limit: int = 10) -> List[ProductSalesStats]:
        """Get product sales statistics."""
        pipeline = [
            {
                "$group": {
                    "_id": "$producto_comprado",
                    "total_vendido": {"$sum": "$cantidad"},
                    "ingresos_totales": {"$sum": "$total"},
                    "ventas_ultimo_mes": {
                        "$sum": {
                            "$cond": [
                                {
                                    "$gte": [
                                        "$fecha",
                                        datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                                    ]
                                },
                                "$cantidad",
                                0
                            ]
                        }
                    }
                }
            },
            {"$sort": {"total_vendido": -1}},
            {"$limit": limit}
        ]
        
        sales_data = await self.db.purchases.aggregate(pipeline).to_list(length=limit)
        
        result = []
        for data in sales_data:
            # Get product info
            product = await self.db.products.find_one({"nombre_producto": data["_id"]})
            if product:
                result.append(ProductSalesStats(
                    product=Product(**product),
                    total_vendido=data["total_vendido"],
                    ingresos_totales=data["ingresos_totales"],
                    ventas_ultimo_mes=data["ventas_ultimo_mes"]
                ))
        
        return result
    
    async def get_stock_chart_data(self) -> Dict[str, Any]:
        """Get stock chart data."""
        # Most sold products
        most_sold_pipeline = [
            {
                "$group": {
                    "_id": "$producto_comprado",
                    "total_vendido": {"$sum": "$cantidad"}
                }
            },
            {"$sort": {"total_vendido": -1}},
            {"$limit": 10}
        ]
        most_sold = await self.db.purchases.aggregate(most_sold_pipeline).to_list(length=10)
        
        # Current stock levels
        products = await self.get_products(limit=20)
        stock_data = [
            {"producto": p.nombre_producto, "stock": p.stock_actual}
            for p in products
        ]
        
        return {
            "most_sold_products": {
                "labels": [item["_id"] for item in most_sold],
                "data": [item["total_vendido"] for item in most_sold]
            },
            "stock_levels": {
                "labels": [item["producto"] for item in stock_data],
                "data": [item["stock"] for item in stock_data]
            }
        }


# Global service instance
stock_service = StockService()

