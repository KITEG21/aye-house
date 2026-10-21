"""Auth feature schemas."""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """Access token response (OAuth2 compatible)."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token lifetime in seconds")
