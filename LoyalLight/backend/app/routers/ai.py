"""
AI endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from ..models.user import User
from ..core.auth import get_current_active_user
from ..core.ai_service_mock import mock_ai_service
from ..services.client_service import client_service
from ..services.purchase_service import purchase_service
from ..services.stock_service import stock_service
from ..services.dashboard_service import dashboard_service
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChurnSuggestionRequest(BaseModel):
    client_id: str


class OfferSuggestionRequest(BaseModel):
    limit: int = 10


class PricingSuggestionRequest(BaseModel):
    product_id: str


@router.post("/churn-suggestions")
async def get_churn_reduction_suggestions(
    request: Request,
    data: ChurnSuggestionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI suggestions to reduce client churn."""
    check_rate_limit(request, f"ai_churn_{current_user.username}")
    
    # Get client data
    client = await client_service.get_client(data.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get AI suggestions using mock service
    suggestions = await mock_ai_service.get_churn_suggestions(int(data.client_id))
    
    return {"suggestions": suggestions}


@router.post("/offer-suggestions")
async def get_offer_suggestions(
    request: Request,
    data: OfferSuggestionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI offer suggestions based on purchase patterns."""
    check_rate_limit(request, f"ai_offers_{current_user.username}")
    
    # Get AI suggestions using mock service
    suggestions = await mock_ai_service.get_offer_suggestions(data.limit)
    
    return {"suggestions": suggestions}


@router.post("/pricing-suggestions")
async def get_pricing_suggestions(
    request: Request,
    data: PricingSuggestionRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI pricing suggestions for products."""
    check_rate_limit(request, f"ai_pricing_{current_user.username}")
    
    # Get product data
    product = await stock_service.get_product(data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get AI suggestions using mock service
    suggestions = await mock_ai_service.get_pricing_suggestions(int(data.product_id))
    
    return {"suggestions": suggestions}


@router.post("/restock-plan")
async def get_restock_plan(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI monthly restock plan suggestions."""
    check_rate_limit(request, f"ai_restock_{current_user.username}")
    
    # Get AI suggestions using mock service
    suggestions = await mock_ai_service.get_restock_plan()
    
    return {"suggestions": suggestions}


@router.post("/global-insights")
async def get_global_insights(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get AI global business insights."""
    check_rate_limit(request, f"ai_insights_{current_user.username}")
    
    # Get AI insights using mock service
    insights = await mock_ai_service.get_global_insights()
    
    return {"insights": insights}

