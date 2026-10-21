"""Property feature repository."""

from typing import Any
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.features.properties.models import Property
from app.features.properties.schemas import PropertyCreate, PropertyFilters, PropertyUpdate
from app.features.zones.models import Municipality, Neighborhood

# Eager-load the full location (reparto > municipio > provincia) for responses
_LOCATION_OPTIONS = (
    joinedload(Property.neighborhood)
    .joinedload(Neighborhood.municipality)
    .joinedload(Municipality.province),
)


class PropertyRepository:
    """Property repository for database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: PropertyCreate) -> Property:
        """Create a new property."""
        prop = Property(**data.model_dump())
        self.session.add(prop)
        await self.session.flush()
        return await self._reload(prop.id)

    async def get_by_id(self, property_id: UUID) -> Property | None:
        """Get property by ID, with its location loaded."""
        result = await self.session.execute(
            select(Property).options(*_LOCATION_OPTIONS).where(Property.id == property_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        filters: PropertyFilters,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Property], int]:
        """Get properties matching the filters, with pagination."""
        conditions = self._conditions(filters)

        count_query = self._join_location(select(func.count(Property.id))).where(*conditions)
        total = (await self.session.execute(count_query)).scalar_one()

        query = (
            self._join_location(select(Property))
            .options(*_LOCATION_OPTIONS)
            .where(*conditions)
            .order_by(Property.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        result = await self.session.execute(query)
        return list(result.unique().scalars().all()), total

    async def update(self, prop: Property, data: PropertyUpdate) -> Property:
        """Update property."""
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(prop, field, value)

        await self.session.flush()
        return await self._reload(prop.id)

    async def delete(self, prop: Property) -> None:
        """Delete property."""
        await self.session.delete(prop)
        await self.session.flush()

    async def _reload(self, property_id: UUID) -> Property:
        # populate_existing refreshes server-generated timestamps and a changed neighborhood
        result = await self.session.execute(
            select(Property)
            .options(*_LOCATION_OPTIONS)
            .where(Property.id == property_id)
            .execution_options(populate_existing=True)
        )
        return result.scalar_one()

    @staticmethod
    def _join_location(query: Select[Any]) -> Select[Any]:
        return (
            query.select_from(Property)
            .join(Neighborhood, Property.neighborhood_id == Neighborhood.id)
            .join(Municipality, Neighborhood.municipality_id == Municipality.id)
        )

    @staticmethod
    def _conditions(filters: PropertyFilters) -> list[Any]:
        conditions: list[Any] = []
        if filters.province_id is not None:
            conditions.append(Municipality.province_id == filters.province_id)
        if filters.municipality_id is not None:
            conditions.append(Neighborhood.municipality_id == filters.municipality_id)
        if filters.neighborhood_id is not None:
            conditions.append(Property.neighborhood_id == filters.neighborhood_id)
        if filters.property_type is not None:
            conditions.append(Property.property_type == filters.property_type)
        if filters.listing_type is not None:
            conditions.append(Property.listing_type == filters.listing_type)
        if filters.status is not None:
            conditions.append(Property.status == filters.status)
        if filters.gas_type is not None:
            conditions.append(Property.gas_type == filters.gas_type)
        if filters.currency is not None:
            conditions.append(Property.currency == filters.currency)
        if filters.min_price is not None:
            conditions.append(Property.price >= filters.min_price)
        if filters.max_price is not None:
            conditions.append(Property.price <= filters.max_price)
        if filters.min_bedrooms is not None:
            conditions.append(Property.bedrooms >= filters.min_bedrooms)
        return conditions
