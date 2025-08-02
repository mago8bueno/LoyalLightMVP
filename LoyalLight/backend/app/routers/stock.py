"""
Stock/Product endpoints.
"""
import os
import uuid
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File
from ..models.product import Product, ProductCreate, ProductUpdate, ProductSalesStats, StockAlert
from ..models.user import User
from ..core.auth import get_current_active_user
from ..services.stock_service import stock_service
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/stock", tags=["stock"])


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: Request,
    product_data: ProductCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new product."""
    check_rate_limit(request)
    
    try:
        return await stock_service.create_product(product_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Product])
async def get_products(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """Get list of products."""
    check_rate_limit(request)
    return await stock_service.get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product)
async def get_product(
    request: Request,
    product_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get product by ID."""
    check_rate_limit(request)
    
    product = await stock_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=Product)
async def update_product(
    request: Request,
    product_id: str,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update product."""
    check_rate_limit(request)
    
    try:
        product = await stock_service.update_product(product_id, product_data)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{product_id}")
async def delete_product(
    request: Request,
    product_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete product."""
    check_rate_limit(request)
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    success = await stock_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"message": "Product deleted successfully"}


@router.post("/{product_id}/upload-image", response_model=Product)
async def upload_product_image(
    request: Request,
    product_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload product image."""
    check_rate_limit(request)
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create uploads directory if it doesn't exist
    upload_dir = "/tmp/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Update product with image URL
    product = await stock_service.upload_product_image(product_id, f"/uploads/{filename}")
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product


@router.get("/analytics/low-stock", response_model=List[Product])
async def get_low_stock_products(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get products with low stock."""
    check_rate_limit(request)
    return await stock_service.get_low_stock_products()


@router.get("/analytics/alerts", response_model=List[StockAlert])
async def get_stock_alerts(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get stock alerts."""
    check_rate_limit(request)
    return await stock_service.get_stock_alerts()


@router.get("/analytics/sales-stats", response_model=List[ProductSalesStats])
async def get_product_sales_stats(
    request: Request,
    limit: int = 10,
    current_user: User = Depends(get_current_active_user)
):
    """Get product sales statistics."""
    check_rate_limit(request)
    return await stock_service.get_product_sales_stats(limit=limit)


@router.get("/analytics/charts", response_model=Dict[str, Any])
async def get_stock_chart_data(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get stock chart data."""
    check_rate_limit(request)
    return await stock_service.get_stock_chart_data()

