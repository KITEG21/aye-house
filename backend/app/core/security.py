"""Security utilities for password hashing and JWT."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# Password hashing (argon2 has no input length limit, unlike bcrypt's 72 bytes)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def dummy_verify_password() -> None:
    """Spend the same time as a real verification, to avoid leaking which users exist."""
    pwd_context.dummy_verify()


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


# JWT
def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token for the given subject (the user ID)."""
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    encoded_jwt: str = jwt.encode(
        {"sub": subject, "exp": expire},
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and validate a JWT access token."""
    payload: dict[str, Any] = jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
    )
    return payload
