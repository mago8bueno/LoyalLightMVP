"""
Rate limiting utilities for API consumption control.
"""
import time
from typing import Dict, Optional
from fastapi import HTTPException, Request
from ..core.config import settings


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, identifier: str, max_requests: int = None, window_seconds: int = 60) -> bool:
        """Check if request is allowed based on rate limits."""
        if max_requests is None:
            max_requests = settings.rate_limit_requests_per_minute
        
        current_time = time.time()
        window_start = current_time - window_seconds
        
        # Initialize or clean old requests
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests outside the window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier] 
            if req_time > window_start
        ]
        
        # Check if under limit
        if len(self.requests[identifier]) >= max_requests:
            return False
        
        # Add current request
        self.requests[identifier].append(current_time)
        return True
    
    def get_reset_time(self, identifier: str, window_seconds: int = 60) -> Optional[float]:
        """Get time when rate limit resets."""
        if identifier not in self.requests or not self.requests[identifier]:
            return None
        
        oldest_request = min(self.requests[identifier])
        return oldest_request + window_seconds


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(request: Request, identifier: str = None):
    """Check rate limit for request."""
    if identifier is None:
        # Use IP address as identifier
        identifier = request.client.host
    
    if not rate_limiter.is_allowed(identifier):
        reset_time = rate_limiter.get_reset_time(identifier)
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "reset_time": reset_time,
                "limit": settings.rate_limit_requests_per_minute
            }
        )

