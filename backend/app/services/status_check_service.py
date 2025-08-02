"""
Status Check service layer.

This module contains business logic for status check operations,
providing an abstraction layer between API routes and database operations.
"""

import logging
from typing import List, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.status_check import StatusCheck, StatusCheckCreate

logger = logging.getLogger(__name__)


class StatusCheckService:
    """
    Service class for status check operations.
    
    Encapsulates business logic for creating, retrieving, and managing
    status check records. Provides clean separation between API layer
    and database operations.
    """
    
    def __init__(self, database: AsyncIOMotorDatabase) -> None:
        """
        Initialize the status check service.
        
        Args:
            database: MongoDB database instance
        """
        self.database = database
        self.collection = database.status_checks
    
    async def create_status_check(
        self, 
        status_check_data: StatusCheckCreate
    ) -> StatusCheck:
        """
        Create a new status check record.
        
        Takes the input data, creates a complete StatusCheck object with
        auto-generated fields, and stores it in the database.
        
        Args:
            status_check_data: Input data for creating status check
            
        Returns:
            StatusCheck: The created status check with all fields populated
            
        Raises:
            Exception: If database operation fails
        """
        try:
            # Create complete status check object with auto-generated fields
            status_check = StatusCheck(**status_check_data.dict())
            
            # Insert into database
            result = await self.collection.insert_one(status_check.dict())
            
            if not result.inserted_id:
                raise Exception("Failed to insert status check into database")
            
            logger.info(
                f"Created status check with ID: {status_check.id} "
                f"for client: {status_check.client_name}"
            )
            
            return status_check
            
        except Exception as e:
            logger.error(f"Error creating status check: {e}")
            raise
    
    async def get_status_checks(
        self, 
        limit: int = 1000,
        skip: int = 0
    ) -> List[StatusCheck]:
        """
        Retrieve status check records.
        
        Fetches status check records from the database with optional
        pagination support.
        
        Args:
            limit: Maximum number of records to return (default: 1000)
            skip: Number of records to skip for pagination (default: 0)
            
        Returns:
            List[StatusCheck]: List of status check records
            
        Raises:
            Exception: If database operation fails
        """
        try:
            # Query database with pagination
            cursor = self.collection.find().skip(skip).limit(limit)
            status_checks_data = await cursor.to_list(length=limit)
            
            # Convert to Pydantic models
            status_checks = [
                StatusCheck(**status_check_data) 
                for status_check_data in status_checks_data
            ]
            
            logger.info(
                f"Retrieved {len(status_checks)} status check records "
                f"(skip={skip}, limit={limit})"
            )
            
            return status_checks
            
        except Exception as e:
            logger.error(f"Error retrieving status checks: {e}")
            raise
    
    async def get_status_check_by_id(
        self, 
        status_check_id: str
    ) -> Optional[StatusCheck]:
        """
        Retrieve a specific status check by ID.
        
        Args:
            status_check_id: Unique identifier of the status check
            
        Returns:
            StatusCheck if found, None otherwise
            
        Raises:
            Exception: If database operation fails
        """
        try:
            status_check_data = await self.collection.find_one(
                {"id": status_check_id}
            )
            
            if not status_check_data:
                logger.info(f"Status check not found with ID: {status_check_id}")
                return None
            
            status_check = StatusCheck(**status_check_data)
            
            logger.info(f"Retrieved status check with ID: {status_check_id}")
            
            return status_check
            
        except Exception as e:
            logger.error(f"Error retrieving status check by ID: {e}")
            raise