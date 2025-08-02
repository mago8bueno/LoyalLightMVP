"""
Purchase endpoints.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from ..models.purchase import Purchase, PurchaseCreate, PurchaseUpdate, PurchaseWithClient
from ..models.user import User
from ..core.auth import get_current_active_user
from ..services.purchase_service import purchase_service
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/purchases", tags=["purchases"])


@router.post("/", response_model=Purchase, status_code=status.HTTP_201_CREATED)
async def create_purchase(
    request: Request,
    purchase_data: PurchaseCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new purchase."""
    check_rate_limit(request)
    
    try:
        return await purchase_service.create_purchase(purchase_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[PurchaseWithClient])
async def get_purchases(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of purchases."""
    check_rate_limit(request)
    return await purchase_service.get_purchases(skip=skip, limit=limit)


@router.get("/{purchase_id}", response_model=Purchase)
async def get_purchase(
    request: Request,
    purchase_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get purchase by ID."""
    check_rate_limit(request)
    
    purchase = await purchase_service.get_purchase(purchase_id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.put("/{purchase_id}", response_model=Purchase)
async def update_purchase(
    request: Request,
    purchase_id: str,
    purchase_data: PurchaseUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update purchase."""
    check_rate_limit(request)
    
    purchase = await purchase_service.update_purchase(purchase_id, purchase_data)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase


@router.delete("/{purchase_id}")
async def delete_purchase(
    request: Request,
    purchase_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete purchase."""
    check_rate_limit(request)
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = await purchase_service.delete_purchase(purchase_id)
    if not success:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    return {"message": "Purchase deleted successfully"}


@router.get("/client/{client_id}", response_model=List[Purchase])
async def get_purchases_by_client(
    request: Request,
    client_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get purchases by client ID."""
    check_rate_limit(request)
    return await purchase_service.get_purchases_by_client(client_id)


@router.get("/analytics/recent", response_model=List[PurchaseWithClient])
async def get_recent_purchases(
    request: Request,
    days: int = 30,
    current_user: User = Depends(get_current_active_user)
):
    """Get recent purchases."""
    check_rate_limit(request)
    return await purchase_service.get_recent_purchases(days=days)


@router.get("/analytics/sales", response_model=Dict[str, Any])
async def get_sales_analytics(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get sales analytics."""
    check_rate_limit(request)
    return await purchase_service.get_sales_analytics()

