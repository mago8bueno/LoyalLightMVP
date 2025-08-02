"""
LoyalLightMVP Server - Legacy Entry Point.

This file maintains the original server.py interface for compatibility
while delegating to the new modular application structure.

DEPRECATED: Use `app.main:app` instead for new deployments.
"""

import logging
import warnings

# Import the new modular application
from app.main import app

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Issue deprecation warning
warnings.warn(
    "server.py is deprecated. Use 'app.main:app' for new deployments. "
    "This compatibility layer will be removed in future versions.",
    DeprecationWarning,
    stacklevel=2
)

logger.info(
    "Loading application via legacy server.py entry point. "
    "Consider updating to use 'app.main:app' directly."
)

# Export the app for backward compatibility
__all__ = ["app"]
