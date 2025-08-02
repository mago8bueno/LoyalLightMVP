"""
Client endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models.client import Client, ClientCreate, ClientUpdate, ClientChurnAnalysis
from ..models.user import User
from ..core.auth import get_current_active_user
from ..services.client_service import client_service
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(
    request: Request,
    client_data: ClientCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new client."""
    check_rate_limit(request)
    
    try:
        return await client_service.create_client(client_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Client])
async def get_clients(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of clients."""
    check_rate_limit(request)
    return await client_service.get_clients(skip=skip, limit=limit)


@router.get("/{client_id}", response_model=Client)
async def get_client(
    request: Request,
    client_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get client by ID."""
    check_rate_limit(request)
    
    client = await client_service.get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=Client)
async def update_client(
    request: Request,
    client_id: str,
    client_data: ClientUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update client."""
    check_rate_limit(request)
    
    try:
        client = await client_service.update_client(client_id, client_data)
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        return client
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{client_id}")
async def delete_client(
    request: Request,
    client_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete client."""
    check_rate_limit(request)
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = await client_service.delete_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    
    return {"message": "Client deleted successfully"}


@router.get("/analytics/top-loyal", response_model=List[Client])
async def get_top_loyal_clients(
    request: Request,
    limit: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Get top loyal clients."""
    check_rate_limit(request)
    return await client_service.get_top_loyal_clients(limit=limit)


@router.get("/analytics/churn-risk", response_model=List[ClientChurnAnalysis])
async def get_churn_risk_clients(
    request: Request,
    limit: int = 5,
    current_user: User = Depends(get_current_active_user)
):
    """Get clients with high churn risk."""
    check_rate_limit(request)
    return await client_service.get_churn_risk_clients(limit=limit)

