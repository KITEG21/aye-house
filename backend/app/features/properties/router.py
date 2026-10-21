"""Property feature router."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.features.properties.dependencies import PropertyServiceDep
from app.features.properties.schemas import (
    PropertyCreate,
    PropertyFilters,
    PropertyListResponse,
    PropertyResponse,
    PropertyUpdate,
)

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post(
    "",
    response_model=PropertyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a property",
)
async def create_property(
    data: PropertyCreate,
    property_service: PropertyServiceDep,
) -> PropertyResponse:
    """Create a property."""
    return await property_service.create_property(data)


@router.get(
    "",
    response_model=PropertyListResponse,
    summary="List properties",
    description="Get a paginated, filterable list of properties, newest first",
)
async def list_properties(
    property_service: PropertyServiceDep,
    filters: Annotated[PropertyFilters, Depends()],
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Page size")] = 20,
) -> PropertyListResponse:
    """List properties."""
    return await property_service.get_properties(filters, page, page_size)


@router.get("/{property_id}", response_model=PropertyResponse, summary="Get property")
async def get_property(
    property_id: UUID,
    property_service: PropertyServiceDep,
) -> PropertyResponse:
    """Get property by ID."""
    return await property_service.get_property(property_id)


@router.patch("/{property_id}", response_model=PropertyResponse, summary="Update property")
async def update_property(
    property_id: UUID,
    data: PropertyUpdate,
    property_service: PropertyServiceDep,
) -> PropertyResponse:
    """Update property."""
    return await property_service.update_property(property_id, data)


@router.delete(
    "/{property_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete property",
)
async def delete_property(
    property_id: UUID,
    property_service: PropertyServiceDep,
) -> None:
    """Delete property."""
    await property_service.delete_property(property_id)
