"""Zone feature dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.features.zones.service import ZoneService


async def get_zone_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ZoneService:
    """Get zone service instance."""
    return ZoneService(session)


# Type aliases for dependency injection
ZoneServiceDep = Annotated[ZoneService, Depends(get_zone_service)]
