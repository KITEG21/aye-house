"""User feature dependencies."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_session
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.features.users.models import User
from app.features.users.service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{get_settings().api_prefix}/auth/login")


async def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    """Get user service instance."""
    return UserService(session)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    """Get current authenticated user."""
    credentials_exception = UnauthorizedError(
        message="Could not validate credentials",
        error_code="INVALID_TOKEN",
    )

    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError) as err:
        raise credentials_exception from err

    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise UnauthorizedError(
            message="Inactive user",
            error_code="INACTIVE_USER",
        )
    return current_user


async def get_current_superuser(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Get current superuser."""
    if not current_user.is_superuser:
        raise ForbiddenError(
            message="Not enough permissions",
            error_code="NOT_SUPERUSER",
        )
    return current_user


# Type aliases for dependency injection
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
CurrentUserDep = Annotated[User, Depends(get_current_active_user)]
SuperUserDep = Annotated[User, Depends(get_current_superuser)]
