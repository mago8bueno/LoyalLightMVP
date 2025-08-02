"""
Dashboard endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, Request
from ..models.dashboard import DashboardMetrics, DashboardData, Alert, ChartData
from ..models.user import User
from ..core.auth import get_current_active_user
from ..services.dashboard_service import dashboard_service
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard metrics."""
    check_rate_limit(request)
    return await dashboard_service.get_dashboard_metrics()


@router.get("/alerts", response_model=List[Alert])
async def get_alerts(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get system alerts."""
    check_rate_limit(request)
    return await dashboard_service.get_alerts()


@router.get("/sales-chart", response_model=ChartData)
async def get_sales_chart_data(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get sales chart data."""
    check_rate_limit(request)
    return await dashboard_service.get_sales_chart_data()


@router.get("/", response_model=DashboardData)
async def get_complete_dashboard_data(
    request: Request,
    current_user: User = Depends(get_current_active_user)
):
    """Get complete dashboard data."""
    check_rate_limit(request)
    return await dashboard_service.get_complete_dashboard_data()

