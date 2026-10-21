"""Auth feature router."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.core.exceptions import UnauthorizedError
from app.core.security import create_access_token
from app.features.auth.schemas import TokenResponse
from app.features.users.dependencies import UserServiceDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Log in",
    description=(
        "OAuth2 password flow. Send `username` (email or username) and `password` as "
        "form data; use the returned token as `Authorization: Bearer <token>`."
    ),
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDep,
) -> TokenResponse:
    """Authenticate a user and return an access token."""
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise UnauthorizedError(
            message="Incorrect username or password",
            error_code="INVALID_CREDENTIALS",
        )
    if not user.is_active:
        raise UnauthorizedError(message="Inactive user", error_code="INACTIVE_USER")

    expire_minutes = get_settings().access_token_expire_minutes
    return TokenResponse(
        access_token=create_access_token(str(user.id)),
        expires_in=expire_minutes * 60,
    )
