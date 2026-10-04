"""Features package initialization."""

from app.features.health import health_router
from app.features.users import users_router

__all__ = ["health_router", "users_router"]
