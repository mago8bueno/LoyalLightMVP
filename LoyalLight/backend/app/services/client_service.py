"""
Client service with business logic.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.client import Client, ClientCreate, ClientUpdate, ClientChurnAnalysis
from ..core.database import get_database


class ClientService:
    """Client service for business logic."""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db or get_database()
    
    async def create_client(self, client_data: ClientCreate) -> Client:
        """Create a new client."""
        client_dict = client_data.dict()
        client_dict.update({
            "_id": str(uuid.uuid4()),
            "fecha_registro": datetime.utcnow(),
            "churn_score": 0.0,
            "total_compras": 0,
            "valor_total": 0.0
        })
        
        # Check if email already exists
        existing_client = await self.db.clients.find_one(
            {"correo_electronico": client_data.correo_electronico}
        )
        if existing_client:
            raise ValueError("Email already exists")
        
        await self.db.clients.insert_one(client_dict)
        return Client(**client_dict)
    
    async def get_client(self, client_id: str) -> Optional[Client]:
        """Get client by ID."""
        client = await self.db.clients.find_one({"_id": client_id})
        return Client(**client) if client else None
    
    async def get_clients(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """Get list of clients."""
        cursor = self.db.clients.find().skip(skip).limit(limit)
        clients = await cursor.to_list(length=limit)
        return [Client(**client) for client in clients]
    
    async def update_client(self, client_id: str, client_data: ClientUpdate) -> Optional[Client]:
        """Update client."""
        update_data = {k: v for k, v in client_data.dict().items() if v is not None}
        
        if not update_data:
            return await self.get_client(client_id)
        
        # Check email uniqueness if updating email
        if "correo_electronico" in update_data:
            existing_client = await self.db.clients.find_one({
                "correo_electronico": update_data["correo_electronico"],
                "_id": {"$ne": client_id}
            })
            if existing_client:
                raise ValueError("Email already exists")
        
        result = await self.db.clients.update_one(
            {"_id": client_id},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_client(client_id)
        return None
    
    async def delete_client(self, client_id: str) -> bool:
        """Delete client."""
        result = await self.db.clients.delete_one({"_id": client_id})
        return result.deleted_count > 0
    
    async def calculate_churn_score(self, client_id: str) -> float:
        """Calculate churn score for a client."""
        # Get client's purchase history
        purchases = await self.db.purchases.find({"cliente_id": client_id}).to_list(length=None)
        
        if not purchases:
            return 0.8  # High churn risk for clients with no purchases
        
        # Simple churn calculation based on recency and frequency
        now = datetime.utcnow()
        last_purchase = max(purchase["fecha"] for purchase in purchases)
        days_since_last_purchase = (now - last_purchase).days
        
        total_purchases = len(purchases)
        avg_days_between_purchases = days_since_last_purchase / max(total_purchases, 1)
        
        # Normalize to 0-1 scale (higher = more likely to churn)
        recency_score = min(days_since_last_purchase / 365, 1.0)  # Max 1 year
        frequency_score = max(0, 1 - (total_purchases / 50))  # Normalize by 50 purchases
        
        churn_score = (recency_score * 0.7) + (frequency_score * 0.3)
        return min(churn_score, 1.0)
    
    async def update_client_metrics(self, client_id: str):
        """Update client metrics (churn score, total purchases, total value)."""
        # Calculate metrics from purchases
        purchases = await self.db.purchases.find({"cliente_id": client_id}).to_list(length=None)
        
        total_compras = len(purchases)
        valor_total = sum(purchase.get("total", 0) for purchase in purchases)
        churn_score = await self.calculate_churn_score(client_id)
        
        # Update client record
        await self.db.clients.update_one(
            {"_id": client_id},
            {
                "$set": {
                    "total_compras": total_compras,
                    "valor_total": valor_total,
                    "churn_score": churn_score
                }
            }
        )
    
    async def get_top_loyal_clients(self, limit: int = 5) -> List[Client]:
        """Get top loyal clients (lowest churn score + highest value)."""
        pipeline = [
            {
                "$addFields": {
                    "loyalty_score": {
                        "$add": [
                            {"$multiply": [{"$subtract": [1, "$churn_score"]}, 0.6]},
                            {"$multiply": [{"$divide": ["$valor_total", 10000]}, 0.4]}
                        ]
                    }
                }
            },
            {"$sort": {"loyalty_score": -1}},
            {"$limit": limit}
        ]
        
        cursor = self.db.clients.aggregate(pipeline)
        clients = await cursor.to_list(length=limit)
        return [Client(**client) for client in clients]
    
    async def get_churn_risk_clients(self, limit: int = 5) -> List[ClientChurnAnalysis]:
        """Get clients with high churn risk."""
        cursor = self.db.clients.find({"churn_score": {"$gte": 0.6}}).sort("churn_score", -1).limit(limit)
        clients = await cursor.to_list(length=limit)
        
        result = []
        for client_data in clients:
            client = Client(**client_data)
            churn_score = client.churn_score
            
            if churn_score >= 0.8:
                risk = "high"
            elif churn_score >= 0.6:
                risk = "medium"
            else:
                risk = "low"
            
            result.append(ClientChurnAnalysis(
                client=client,
                churn_risk=risk,
                churn_score=churn_score
            ))
        
        return result


# Global service instance
client_service = ClientService()

