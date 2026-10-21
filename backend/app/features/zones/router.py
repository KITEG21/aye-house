"""Zone feature router.

Zones are read-only reference data loaded by the seeder (`python -m app.cli seed-zones`).
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.features.zones.dependencies import ZoneServiceDep
from app.features.zones.schemas import (
    MunicipalityResponse,
    NeighborhoodResponse,
    ProvinceResponse,
)

router = APIRouter(tags=["zones"])


# Provinces
@router.get("/provinces", response_model=list[ProvinceResponse], summary="List provinces")
async def list_provinces(zone_service: ZoneServiceDep) -> list[ProvinceResponse]:
    """List all provinces."""
    return await zone_service.get_provinces()


@router.get("/provinces/{province_id}", response_model=ProvinceResponse, summary="Get province")
async def get_province(province_id: UUID, zone_service: ZoneServiceDep) -> ProvinceResponse:
    """Get province by ID."""
    return await zone_service.get_province(province_id)


# Municipalities
@router.get(
    "/municipalities", response_model=list[MunicipalityResponse], summary="List municipalities"
)
async def list_municipalities(
    zone_service: ZoneServiceDep,
    province_id: Annotated[UUID | None, Query(description="Filter by province")] = None,
) -> list[MunicipalityResponse]:
    """List municipalities."""
    return await zone_service.get_municipalities(province_id)


@router.get(
    "/municipalities/{municipality_id}",
    response_model=MunicipalityResponse,
    summary="Get municipality",
)
async def get_municipality(
    municipality_id: UUID, zone_service: ZoneServiceDep
) -> MunicipalityResponse:
    """Get municipality by ID."""
    return await zone_service.get_municipality(municipality_id)


# Neighborhoods
@router.get(
    "/neighborhoods", response_model=list[NeighborhoodResponse], summary="List neighborhoods"
)
async def list_neighborhoods(
    zone_service: ZoneServiceDep,
    municipality_id: Annotated[UUID | None, Query(description="Filter by municipality")] = None,
) -> list[NeighborhoodResponse]:
    """List neighborhoods."""
    return await zone_service.get_neighborhoods(municipality_id)


@router.get(
    "/neighborhoods/{neighborhood_id}",
    response_model=NeighborhoodResponse,
    summary="Get neighborhood",
)
async def get_neighborhood(
    neighborhood_id: UUID, zone_service: ZoneServiceDep
) -> NeighborhoodResponse:
    """Get neighborhood by ID."""
    return await zone_service.get_neighborhood(neighborhood_id)
