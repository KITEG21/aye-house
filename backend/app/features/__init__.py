"""Features package initialization."""

from app.features.auth import auth_router
from app.features.health import health_router
from app.features.properties import properties_router
from app.features.users import users_router
from app.features.zones import zones_router

__all__ = ["auth_router", "health_router", "properties_router", "users_router", "zones_router"]
