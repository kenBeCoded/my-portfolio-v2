"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for login endpoint."""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class Token(BaseModel):
    """Schema for the JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token payload."""
    username: str | None = None
