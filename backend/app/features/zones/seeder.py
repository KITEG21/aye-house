"""Zone seeder.

Zones are fixed reference data: they are not editable through the API and are
loaded from `seed_data.ZONES`. The seeder is idempotent; it only inserts what is
missing, so it is safe to re-run after adding entries to the data file.
"""

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.zones.repository import ZoneRepository
from app.features.zones.seed_data import ZONES


@dataclass
class SeedResult:
    """Number of rows inserted per level."""

    provinces: int = 0
    municipalities: int = 0
    neighborhoods: int = 0


async def seed_zones(session: AsyncSession) -> SeedResult:
    """Insert any provinces, municipalities and neighborhoods that are missing."""
    repository = ZoneRepository(session)
    result = SeedResult()

    for province_name, municipalities in ZONES.items():
        province = await repository.get_province_by_name(province_name)
        if province is None:
            province = await repository.create_province(province_name)
            result.provinces += 1

        for municipality_name, neighborhoods in municipalities.items():
            municipality = await repository.get_municipality_by_name(municipality_name, province.id)
            if municipality is None:
                municipality = await repository.create_municipality(municipality_name, province.id)
                result.municipalities += 1

            for neighborhood_name in neighborhoods:
                if not await repository.get_neighborhood_by_name(
                    neighborhood_name, municipality.id
                ):
                    await repository.create_neighborhood(neighborhood_name, municipality.id)
                    result.neighborhoods += 1

    return result
