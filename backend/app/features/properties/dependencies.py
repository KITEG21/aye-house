"""Property feature dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.features.properties.service import PropertyService


async def get_property_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PropertyService:
    """Get property service instance."""
    return PropertyService(session)


# Type aliases for dependency injection
PropertyServiceDep = Annotated[PropertyService, Depends(get_property_service)]
