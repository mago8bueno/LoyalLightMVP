"""
Mock database service for development without MongoDB
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

class MockDatabase:
    def __init__(self):
        # Mock data storage
        self.clients = []
        self.purchases = []
        self.products = []
        self.users = [
            {
                "id": "1",
                "username": "admin",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
                "role": "admin",
                "is_active": True
            }
        ]
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for testing"""
        # Sample clients
        sample_clients = [
            {
                "id": "1",
                "nombre": "Juan",
                "apellido": "Pérez",
                "correo_electronico": "juan.perez@email.com",
                "fecha_registro": datetime.now() - timedelta(days=30),
                "total_compras": 5,
                "valor_total": 1250.50,
                "churn_score": 0.2
            },
            {
                "id": "2",
                "nombre": "María",
                "apellido": "García",
                "correo_electronico": "maria.garcia@email.com",
                "fecha_registro": datetime.now() - timedelta(days=45),
                "total_compras": 8,
                "valor_total": 2100.75,
                "churn_score": 0.1
            },
            {
                "id": "3",
                "nombre": "Carlos",
                "apellido": "López",
                "correo_electronico": "carlos.lopez@email.com",
                "fecha_registro": datetime.now() - timedelta(days=60),
                "total_compras": 2,
                "valor_total": 450.25,
                "churn_score": 0.8
            }
        ]
        
        # Sample products
        sample_products = [
            {
                "id": "1",
                "nombre_producto": "Laptop Gaming",
                "precio": 1299.99,
                "stock_actual": 15,
                "stock_minimo": 5,
                "fecha_creacion": datetime.now() - timedelta(days=20),
                "imagen_url": None
            },
            {
                "id": "2",
                "nombre_producto": "Mouse Inalámbrico",
                "precio": 49.99,
                "stock_actual": 3,
                "stock_minimo": 10,
                "fecha_creacion": datetime.now() - timedelta(days=15),
                "imagen_url": None
            },
            {
                "id": "3",
                "nombre_producto": "Teclado Mecánico",
                "precio": 129.99,
                "stock_actual": 25,
                "stock_minimo": 8,
                "fecha_creacion": datetime.now() - timedelta(days=10),
                "imagen_url": None
            }
        ]
        
        # Sample purchases
        sample_purchases = [
            {
                "id": "1",
                "producto_comprado": "Laptop Gaming",
                "cliente_id": "1",
                "cantidad": 1,
                "precio_unitario": 1299.99,
                "total": 1299.99,
                "fecha": datetime.now() - timedelta(days=5),
                "cliente_nombre": "Juan",
                "cliente_apellido": "Pérez"
            },
            {
                "id": "2",
                "producto_comprado": "Mouse Inalámbrico",
                "cliente_id": "2",
                "cantidad": 2,
                "precio_unitario": 49.99,
                "total": 99.98,
                "fecha": datetime.now() - timedelta(days=3),
                "cliente_nombre": "María",
                "cliente_apellido": "García"
            }
        ]
        
        self.clients = sample_clients
        self.products = sample_products
        self.purchases = sample_purchases
        
        # Add more users
        for i in range(1, 11):
            self.users.append({
                "id": str(i + 1),
                "username": f"cliente{i}",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # secret
                "role": "client",
                "is_active": True
            })
    
    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        for user in self.users:
            if user["username"] == username:
                return user
        return None
    
    async def get_clients(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all clients"""
        return self.clients[skip:skip + limit]
    
    async def get_client_by_id(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        for client in self.clients:
            if client["id"] == client_id:
                return client
        return None
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new client"""
        new_id = str(len(self.clients) + 1)
        client = {
            "id": new_id,
            "fecha_registro": datetime.now(),
            "total_compras": 0,
            "valor_total": 0.0,
            "churn_score": random.uniform(0.1, 0.3),
            **client_data
        }
        self.clients.append(client)
        return client
    
    async def update_client(self, client_id: str, client_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update client"""
        for i, client in enumerate(self.clients):
            if client["id"] == client_id:
                self.clients[i].update(client_data)
                return self.clients[i]
        return None
    
    async def delete_client(self, client_id: str) -> bool:
        """Delete client"""
        for i, client in enumerate(self.clients):
            if client["id"] == client_id:
                del self.clients[i]
                return True
        return False
    
    async def get_products(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all products"""
        return self.products[skip:skip + limit]
    
    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID"""
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new product"""
        new_id = str(len(self.products) + 1)
        product = {
            "id": new_id,
            "fecha_creacion": datetime.now(),
            "imagen_url": None,
            **product_data
        }
        self.products.append(product)
        return product
    
    async def update_product(self, product_id: str, product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update product"""
        for i, product in enumerate(self.products):
            if product["id"] == product_id:
                self.products[i].update(product_data)
                return self.products[i]
        return None
    
    async def delete_product(self, product_id: str) -> bool:
        """Delete product"""
        for i, product in enumerate(self.products):
            if product["id"] == product_id:
                del self.products[i]
                return True
        return False
    
    async def get_purchases(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all purchases"""
        return self.purchases[skip:skip + limit]
    
    async def get_purchase_by_id(self, purchase_id: str) -> Optional[Dict[str, Any]]:
        """Get purchase by ID"""
        for purchase in self.purchases:
            if purchase["id"] == purchase_id:
                return purchase
        return None
    
    async def create_purchase(self, purchase_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new purchase"""
        new_id = str(len(self.purchases) + 1)
        
        # Get client info
        client = await self.get_client_by_id(purchase_data["cliente_id"])
        
        purchase = {
            "id": new_id,
            "total": purchase_data["cantidad"] * purchase_data["precio_unitario"],
            "cliente_nombre": client["nombre"] if client else "Desconocido",
            "cliente_apellido": client["apellido"] if client else "",
            **purchase_data
        }
        self.purchases.append(purchase)
        
        # Update client stats
        if client:
            await self.update_client(client["id"], {
                "total_compras": client["total_compras"] + 1,
                "valor_total": client["valor_total"] + purchase["total"]
            })
        
        return purchase
    
    async def update_purchase(self, purchase_id: str, purchase_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update purchase"""
        for i, purchase in enumerate(self.purchases):
            if purchase["id"] == purchase_id:
                # Recalculate total
                if "cantidad" in purchase_data or "precio_unitario" in purchase_data:
                    cantidad = purchase_data.get("cantidad", purchase["cantidad"])
                    precio = purchase_data.get("precio_unitario", purchase["precio_unitario"])
                    purchase_data["total"] = cantidad * precio
                
                self.purchases[i].update(purchase_data)
                return self.purchases[i]
        return None
    
    async def delete_purchase(self, purchase_id: str) -> bool:
        """Delete purchase"""
        for i, purchase in enumerate(self.purchases):
            if purchase["id"] == purchase_id:
                del self.purchases[i]
                return True
        return False

# Global instance
mock_db = MockDatabase()

