"""
Database connection and configuration.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .config import settings


class DatabaseManager:
    """Database connection manager."""
    
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database: AsyncIOMotorDatabase = None
    
    async def connect_to_database(self):
        """Create database connection."""
        self.client = AsyncIOMotorClient(settings.mongo_url)
        self.database = self.client[settings.db_name]
        
        # Create indexes
        await self._create_indexes()
    
    async def close_database_connection(self):
        """Close database connection."""
        if self.client:
            self.client.close()
    
    async def _create_indexes(self):
        """Create database indexes for better performance."""
        # Users collection indexes
        await self.database.users.create_index("username", unique=True)
        
        # Clients collection indexes
        await self.database.clients.create_index("correo_electronico", unique=True)
        await self.database.clients.create_index("churn_score")
        
        # Purchases collection indexes
        await self.database.purchases.create_index("cliente_id")
        await self.database.purchases.create_index("fecha")
        await self.database.purchases.create_index("producto_comprado")
        
        # Products collection indexes
        await self.database.products.create_index("nombre_producto", unique=True)
        await self.database.products.create_index("stock_actual")


# Global database manager instance
db_manager = DatabaseManager()


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    return db_manager.database

