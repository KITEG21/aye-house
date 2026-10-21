"""Property feature schemas."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.features.properties.models import (
    Currency,
    GasType,
    ListingType,
    PropertyStatus,
    PropertyType,
)
from app.features.zones.schemas import NeighborhoodSummary


class PropertyBase(BaseModel):
    """Base property schema."""

    title: str = Field(..., min_length=1, max_length=255, description="Listing title")
    description: str | None = Field(None, description="Free-text description")
    property_type: PropertyType = Field(..., description="Property type")
    listing_type: ListingType = Field(..., description="For sale or for rent")
    price: Decimal = Field(
        ..., gt=0, max_digits=14, decimal_places=2, description="Sale price or monthly rent"
    )
    currency: Currency = Field(Currency.USD, description="Price currency")
    area_m2: Decimal | None = Field(
        None, gt=0, max_digits=10, decimal_places=2, description="Area in m²"
    )
    bedrooms: int | None = Field(None, ge=0, description="Number of bedrooms")
    bathrooms: int | None = Field(None, ge=0, description="Number of bathrooms")
    gas_type: GasType = Field(..., description="Gas supply: piped (de la calle) or cylinder")
    address: str | None = Field(None, max_length=500, description="Street address")


class PropertyCreate(PropertyBase):
    """Property creation schema."""

    neighborhood_id: UUID = Field(..., description="Neighborhood (reparto) ID")
    status: PropertyStatus = Field(PropertyStatus.AVAILABLE, description="Listing status")


class PropertyUpdate(BaseModel):
    """Property update schema."""

    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    property_type: PropertyType | None = None
    listing_type: ListingType | None = None
    status: PropertyStatus | None = None
    price: Decimal | None = Field(None, gt=0, max_digits=14, decimal_places=2)
    currency: Currency | None = None
    area_m2: Decimal | None = Field(None, gt=0, max_digits=10, decimal_places=2)
    bedrooms: int | None = Field(None, ge=0)
    bathrooms: int | None = Field(None, ge=0)
    gas_type: GasType | None = None
    address: str | None = Field(None, max_length=500)
    neighborhood_id: UUID | None = None


class PropertyResponse(PropertyBase):
    """Property response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: PropertyStatus
    neighborhood: NeighborhoodSummary
    created_at: datetime
    updated_at: datetime


class PropertyFilters(BaseModel):
    """Filters for listing properties."""

    province_id: UUID | None = None
    municipality_id: UUID | None = None
    neighborhood_id: UUID | None = None
    property_type: PropertyType | None = None
    listing_type: ListingType | None = None
    status: PropertyStatus | None = None
    gas_type: GasType | None = None
    currency: Currency | None = None
    min_price: Decimal | None = Field(None, ge=0)
    max_price: Decimal | None = Field(None, ge=0)
    min_bedrooms: int | None = Field(None, ge=0)


class PropertyListResponse(BaseModel):
    """Property list response schema."""

    properties: list[PropertyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
