"""Zone feature service.

Zones are read-only through the API; they are loaded by `app.features.zones.seeder`.
"""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.features.zones.models import Municipality, Neighborhood, Province
from app.features.zones.repository import ZoneRepository
from app.features.zones.schemas import (
    MunicipalityResponse,
    NeighborhoodResponse,
    ProvinceResponse,
)


class ZoneService:
    """Zone service for business logic."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ZoneRepository(session)

    # Lookups that raise when missing (also used by the properties feature)
    async def get_province_or_404(self, province_id: UUID) -> Province:
        """Get province or raise NotFoundError."""
        province = await self.repository.get_province(province_id)
        if not province:
            raise NotFoundError(
                message="Province not found",
                error_code="PROVINCE_NOT_FOUND",
                details={"province_id": str(province_id)},
            )
        return province

    async def get_municipality_or_404(self, municipality_id: UUID) -> Municipality:
        """Get municipality or raise NotFoundError."""
        municipality = await self.repository.get_municipality(municipality_id)
        if not municipality:
            raise NotFoundError(
                message="Municipality not found",
                error_code="MUNICIPALITY_NOT_FOUND",
                details={"municipality_id": str(municipality_id)},
            )
        return municipality

    async def get_neighborhood_or_404(self, neighborhood_id: UUID) -> Neighborhood:
        """Get neighborhood or raise NotFoundError."""
        neighborhood = await self.repository.get_neighborhood(neighborhood_id)
        if not neighborhood:
            raise NotFoundError(
                message="Neighborhood not found",
                error_code="NEIGHBORHOOD_NOT_FOUND",
                details={"neighborhood_id": str(neighborhood_id)},
            )
        return neighborhood

    # Provinces
    async def get_province(self, province_id: UUID) -> ProvinceResponse:
        """Get province by ID."""
        return ProvinceResponse.model_validate(await self.get_province_or_404(province_id))

    async def get_provinces(self) -> list[ProvinceResponse]:
        """Get all provinces."""
        provinces = await self.repository.get_provinces()
        return [ProvinceResponse.model_validate(p) for p in provinces]

    # Municipalities
    async def get_municipality(self, municipality_id: UUID) -> MunicipalityResponse:
        """Get municipality by ID."""
        return MunicipalityResponse.model_validate(
            await self.get_municipality_or_404(municipality_id)
        )

    async def get_municipalities(
        self, province_id: UUID | None = None
    ) -> list[MunicipalityResponse]:
        """Get municipalities, optionally filtered by province."""
        municipalities = await self.repository.get_municipalities(province_id)
        return [MunicipalityResponse.model_validate(m) for m in municipalities]

    # Neighborhoods
    async def get_neighborhood(self, neighborhood_id: UUID) -> NeighborhoodResponse:
        """Get neighborhood by ID."""
        return NeighborhoodResponse.model_validate(
            await self.get_neighborhood_or_404(neighborhood_id)
        )

    async def get_neighborhoods(
        self, municipality_id: UUID | None = None
    ) -> list[NeighborhoodResponse]:
        """Get neighborhoods, optionally filtered by municipality."""
        neighborhoods = await self.repository.get_neighborhoods(municipality_id)
        return [NeighborhoodResponse.model_validate(n) for n in neighborhoods]
