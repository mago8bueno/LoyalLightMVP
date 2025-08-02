"""
Authentication endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from ..models.user import UserLogin, Token, User
from ..core.auth import authenticate_user, create_access_token, get_current_active_user
from ..core.config import settings
from ..utils.rate_limiter import check_rate_limit


router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/login", response_model=Token)
async def login(request: Request, user_credentials: UserLogin):
    """Authenticate user and return access token."""
    check_rate_limit(request, f"login_{user_credentials.username}")
    
    user = await authenticate_user(user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }


@router.get("/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_active_user)):
    """Get current user information."""
    return User(
        id=current_user["id"],
        username=current_user["username"],
        role=current_user["role"],
        is_active=current_user.get("is_active", True)
    )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_active_user)):
    """Logout user (client-side token removal)."""
    return {"message": "Successfully logged out"}

