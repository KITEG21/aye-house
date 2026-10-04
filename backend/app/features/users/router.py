"""User feature router."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.features.users.dependencies import (
    CurrentUserDep,
    SuperUserDep,
    UserServiceDep,
)
from app.features.users.schemas import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Register a new user account",
)
async def create_user(
    user_data: UserCreate,
    user_service: UserServiceDep,
) -> UserResponse:
    """Create a new user."""
    return await user_service.create_user(user_data)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get the profile of the currently authenticated user",
)
async def get_current_user_profile(
    current_user: CurrentUserDep,
) -> UserResponse:
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get a user by their ID (superuser only)",
)
async def get_user(
    user_id: UUID,
    user_service: UserServiceDep,
    _: SuperUserDep,
) -> UserResponse:
    """Get user by ID."""
    return await user_service.get_user(user_id)


@router.get(
    "",
    response_model=UserListResponse,
    summary="List users",
    description="Get a paginated list of users (superuser only)",
)
async def list_users(
    user_service: UserServiceDep,
    _: SuperUserDep,
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Page size")] = 20,
    is_active: Annotated[bool | None, Query(description="Filter by active status")] = None,
) -> UserListResponse:
    """List users with pagination."""
    return await user_service.get_users(page, page_size, is_active)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update a user by ID (superuser only)",
)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserServiceDep,
    _: SuperUserDep,
) -> UserResponse:
    """Update user."""
    return await user_service.update_user(user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by ID (superuser only)",
)
async def delete_user(
    user_id: UUID,
    user_service: UserServiceDep,
    _: SuperUserDep,
) -> None:
    """Delete user."""
    await user_service.delete_user(user_id)
