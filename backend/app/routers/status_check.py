"""
Status Check API routes.

This module defines FastAPI routes for status check operations,
maintaining the exact same endpoints as the original implementation.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.models.status_check import StatusCheck, StatusCheckCreate
from app.services.status_check_service import StatusCheckService

logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()


async def get_status_check_service(
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> StatusCheckService:
    """
    Dependency to get status check service instance.
    
    Args:
        database: MongoDB database instance
        
    Returns:
        StatusCheckService: Configured service instance
    """
    return StatusCheckService(database)


@router.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint - Health check.
    
    Simple endpoint to verify API is running. Maintains exact same
    response as original implementation.
    
    Returns:
        dict: Simple message confirming API is working
    """
    logger.info("Root endpoint accessed")
    return {"message": "Hello World"}


@router.post("/status", response_model=StatusCheck)
async def create_status_check(
    input_data: StatusCheckCreate,
    service: StatusCheckService = Depends(get_status_check_service)
) -> StatusCheck:
    """
    Create a new status check.
    
    Creates a new status check record with the provided client name.
    Auto-generates ID and timestamp fields.
    
    Args:
        input_data: Status check creation data
        service: Status check service instance
        
    Returns:
        StatusCheck: The created status check with all fields
        
    Raises:
        HTTPException: If creation fails
    """
    try:
        logger.info(f"Creating status check for client: {input_data.client_name}")
        
        status_check = await service.create_status_check(input_data)
        
        logger.info(f"Successfully created status check with ID: {status_check.id}")
        
        return status_check
        
    except Exception as e:
        logger.error(f"Failed to create status check: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create status check"
        )


@router.get("/status", response_model=List[StatusCheck])
async def get_status_checks(
    service: StatusCheckService = Depends(get_status_check_service)
) -> List[StatusCheck]:
    """
    Retrieve all status checks.
    
    Fetches all status check records from the database. Maintains exact
    same behavior as original implementation (returns up to 1000 records).
    
    Args:
        service: Status check service instance
        
    Returns:
        List[StatusCheck]: List of all status check records
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        logger.info("Retrieving all status checks")
        
        status_checks = await service.get_status_checks(limit=1000)
        
        logger.info(f"Successfully retrieved {len(status_checks)} status checks")
        
        return status_checks
        
    except Exception as e:
        logger.error(f"Failed to retrieve status checks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve status checks"
        )