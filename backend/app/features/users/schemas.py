"""User feature schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., min_length=3, max_length=100, description="Username")
    full_name: str | None = Field(None, max_length=255, description="Full name")


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8, max_length=100, description="Password")


class UserUpdate(BaseModel):
    """User update schema."""

    email: EmailStr | None = Field(None, description="User email")
    username: str | None = Field(None, min_length=3, max_length=100, description="Username")
    full_name: str | None = Field(None, max_length=255, description="Full name")
    is_active: bool | None = Field(None, description="Whether user is active")
    is_superuser: bool | None = Field(None, description="Whether user is superuser")


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserListResponse(BaseModel):
    """User list response schema."""

    users: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
