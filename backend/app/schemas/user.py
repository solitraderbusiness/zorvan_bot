"""User schemas."""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    """User update schema."""

    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """User response schema."""

    id: int
    is_admin: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """User login schema."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token schema."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data schema."""

    email: Optional[str] = None


class PasswordChange(BaseModel):
    """Password change schema."""

    old_password: str
    new_password: str
