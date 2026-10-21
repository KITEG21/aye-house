"""Property feature service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationError
from app.features.properties.models import ListingType, Property, PropertyStatus
from app.features.properties.repository import PropertyRepository
from app.features.properties.schemas import (
    PropertyCreate,
    PropertyFilters,
    PropertyListResponse,
    PropertyResponse,
    PropertyUpdate,
)
from app.features.zones.service import ZoneService

# Final statuses that only make sense for one listing type
_STATUS_LISTING_TYPE = {
    PropertyStatus.SOLD: ListingType.SALE,
    PropertyStatus.RENTED: ListingType.RENTAL,
}


class PropertyService:
    """Property service for business logic."""

    def __init__(self, session: AsyncSession):
        self.repository = PropertyRepository(session)
        self.zone_service = ZoneService(session)

    async def create_property(self, data: PropertyCreate) -> PropertyResponse:
        """Create a new property."""
        await self.zone_service.get_neighborhood_or_404(data.neighborhood_id)
        self._check_status(data.status, data.listing_type)

        prop = await self.repository.create(data)
        return PropertyResponse.model_validate(prop)

    async def get_property(self, property_id: UUID) -> PropertyResponse:
        """Get property by ID."""
        return PropertyResponse.model_validate(await self._get_or_404(property_id))

    async def get_properties(
        self,
        filters: PropertyFilters,
        page: int = 1,
        page_size: int = 20,
    ) -> PropertyListResponse:
        """Get properties with filters and pagination."""
        properties, total = await self.repository.get_all(filters, page, page_size)

        return PropertyListResponse(
            properties=[PropertyResponse.model_validate(p) for p in properties],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    async def update_property(self, property_id: UUID, data: PropertyUpdate) -> PropertyResponse:
        """Update property."""
        prop = await self._get_or_404(property_id)

        if data.neighborhood_id and data.neighborhood_id != prop.neighborhood_id:
            await self.zone_service.get_neighborhood_or_404(data.neighborhood_id)

        self._check_status(
            data.status or prop.status,
            data.listing_type or prop.listing_type,
        )

        prop = await self.repository.update(prop, data)
        return PropertyResponse.model_validate(prop)

    async def delete_property(self, property_id: UUID) -> None:
        """Delete property."""
        prop = await self._get_or_404(property_id)
        await self.repository.delete(prop)

    async def _get_or_404(self, property_id: UUID) -> Property:
        prop = await self.repository.get_by_id(property_id)
        if not prop:
            raise NotFoundError(
                message="Property not found",
                error_code="PROPERTY_NOT_FOUND",
                details={"property_id": str(property_id)},
            )
        return prop

    @staticmethod
    def _check_status(status: PropertyStatus, listing_type: ListingType) -> None:
        required = _STATUS_LISTING_TYPE.get(status)
        if required is not None and required != listing_type:
            raise ValidationError(
                message=f"Status '{status}' is only valid for '{required}' listings",
                error_code="INVALID_STATUS_FOR_LISTING_TYPE",
                details={"status": status.value, "listing_type": listing_type.value},
            )
