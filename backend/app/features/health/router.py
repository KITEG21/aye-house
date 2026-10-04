"""Health feature router."""

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_session
from app.features.health.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])
settings = get_settings()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Detailed health check",
    description="Check the health of the application and its dependencies",
)
async def health_check(
    session: AsyncSession = Depends(get_session),
) -> HealthResponse:
    """Check application and database health."""
    # Check database connection
    try:
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get(
    "/ready",
    summary="Readiness check",
    description="Check if the application is ready to serve requests",
)
async def readiness_check(
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    """Check if application is ready (for Kubernetes readiness probe)."""
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}
