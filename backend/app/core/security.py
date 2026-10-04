"""Security utilities for password hashing and JWT."""
import importlib.util
from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

# Password hashing
# Use argon2 if available, otherwise fallback to bcrypt with workaround
if importlib.util.find_spec("argon2") is not None:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
else:
    # Fallback to bcrypt with workaround for passlib/bcrypt compatibility issue
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # bcrypt has a 72-byte limit, truncate if necessary
    # This is a workaround for passlib/bcrypt compatibility issues
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.hash(password)


# JWT
def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(
        to_encode,
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
