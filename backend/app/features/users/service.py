"""User feature service."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import get_password_hash, verify_password
from app.features.users.models import User
from app.features.users.repository import UserRepository
from app.features.users.schemas import UserCreate, UserListResponse, UserResponse, UserUpdate


class UserService:
    """User service for business logic."""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        # Check if email exists
        existing_email = await self.repository.get_by_email(user_data.email)
        if existing_email:
            raise ConflictError(
                message="Email already registered",
                error_code="EMAIL_EXISTS",
                details={"email": user_data.email},
            )

        # Check if username exists
        existing_username = await self.repository.get_by_username(user_data.username)
        if existing_username:
            raise ConflictError(
                message="Username already taken",
                error_code="USERNAME_EXISTS",
                details={"username": user_data.username},
            )

        # Hash password
        hashed_password = get_password_hash(user_data.password)

        # Create user
        user = await self.repository.create(user_data, hashed_password)
        return UserResponse.model_validate(user)

    async def get_user(self, user_id: UUID) -> UserResponse:
        """Get user by ID."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(
                message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id},
            )
        return UserResponse.model_validate(user)

    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email (for authentication)."""
        return await self.repository.get_by_email(email)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        """Authenticate user with email and password."""
        user = await self.repository.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_users(
        self,
        page: int = 1,
        page_size: int = 20,
        is_active: bool | None = None,
    ) -> UserListResponse:
        """Get all users with pagination."""
        users, total = await self.repository.get_all(page, page_size, is_active)

        return UserListResponse(
            users=[UserResponse.model_validate(user) for user in users],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    async def update_user(self, user_id: UUID, user_data: UserUpdate) -> UserResponse:
        """Update user."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(
                message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id},
            )

        # Check email uniqueness if changing
        if user_data.email and user_data.email != user.email:
            existing = await self.repository.get_by_email(user_data.email)
            if existing:
                raise ConflictError(
                    message="Email already registered",
                    error_code="EMAIL_EXISTS",
                    details={"email": user_data.email},
                )

        # Check username uniqueness if changing
        if user_data.username and user_data.username != user.username:
            existing = await self.repository.get_by_username(user_data.username)
            if existing:
                raise ConflictError(
                    message="Username already taken",
                    error_code="USERNAME_EXISTS",
                    details={"username": user_data.username},
                )

        updated_user = await self.repository.update(user, user_data)
        return UserResponse.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> None:
        """Delete user."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError(
                message="User not found",
                error_code="USER_NOT_FOUND",
                details={"user_id": user_id},
            )

        await self.repository.delete(user)
