"""Zone feature repository."""

from typing import TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.features.zones.models import Municipality, Neighborhood, Province

ModelT = TypeVar("ModelT", bound=Base)


class ZoneRepository:
    """Zone repository for provinces, municipalities and neighborhoods."""

    def __init__(self, session: AsyncSession):
        self.session = session

    # Shared helpers
    async def _add(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    # Provinces
    async def create_province(self, name: str) -> Province:
        """Create a new province."""
        return await self._add(Province(name=name))

    async def get_province(self, province_id: UUID) -> Province | None:
        """Get province by ID."""
        return await self.session.get(Province, province_id)

    async def get_province_by_name(self, name: str) -> Province | None:
        """Get province by name."""
        result = await self.session.execute(select(Province).where(Province.name == name))
        return result.scalar_one_or_none()

    async def get_provinces(self) -> list[Province]:
        """Get all provinces ordered by name."""
        result = await self.session.execute(select(Province).order_by(Province.name))
        return list(result.scalars().all())

    # Municipalities
    async def create_municipality(self, name: str, province_id: UUID) -> Municipality:
        """Create a new municipality."""
        return await self._add(Municipality(name=name, province_id=province_id))

    async def get_municipality(self, municipality_id: UUID) -> Municipality | None:
        """Get municipality by ID."""
        return await self.session.get(Municipality, municipality_id)

    async def get_municipality_by_name(self, name: str, province_id: UUID) -> Municipality | None:
        """Get municipality by name within a province."""
        result = await self.session.execute(
            select(Municipality).where(
                Municipality.name == name,
                Municipality.province_id == province_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_municipalities(self, province_id: UUID | None = None) -> list[Municipality]:
        """Get municipalities ordered by name, optionally filtered by province."""
        query = select(Municipality).order_by(Municipality.name)
        if province_id is not None:
            query = query.where(Municipality.province_id == province_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    # Neighborhoods
    async def create_neighborhood(self, name: str, municipality_id: UUID) -> Neighborhood:
        """Create a new neighborhood."""
        return await self._add(Neighborhood(name=name, municipality_id=municipality_id))

    async def get_neighborhood(self, neighborhood_id: UUID) -> Neighborhood | None:
        """Get neighborhood by ID."""
        return await self.session.get(Neighborhood, neighborhood_id)

    async def get_neighborhood_by_name(
        self, name: str, municipality_id: UUID
    ) -> Neighborhood | None:
        """Get neighborhood by name within a municipality."""
        result = await self.session.execute(
            select(Neighborhood).where(
                Neighborhood.name == name,
                Neighborhood.municipality_id == municipality_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_neighborhoods(self, municipality_id: UUID | None = None) -> list[Neighborhood]:
        """Get neighborhoods ordered by name, optionally filtered by municipality."""
        query = select(Neighborhood).order_by(Neighborhood.name)
        if municipality_id is not None:
            query = query.where(Neighborhood.municipality_id == municipality_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())
