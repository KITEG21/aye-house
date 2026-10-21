"""Zone feature schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# Province
class ProvinceResponse(BaseModel):
    """Province response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime


# Municipality
class MunicipalityResponse(BaseModel):
    """Municipality response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    province_id: UUID
    created_at: datetime
    updated_at: datetime


# Neighborhood
class NeighborhoodResponse(BaseModel):
    """Neighborhood response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    municipality_id: UUID
    created_at: datetime
    updated_at: datetime


# Nested summaries, used to embed a full location in other responses
class ProvinceSummary(BaseModel):
    """Province summary schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class MunicipalitySummary(BaseModel):
    """Municipality summary schema, including its province."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    province: ProvinceSummary


class NeighborhoodSummary(BaseModel):
    """Neighborhood summary schema, including its municipality and province."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    municipality: MunicipalitySummary
