"""Class schemas."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ClassBase(BaseModel):
    """Base class schema."""

    name: str
    description: Optional[str] = None


class ClassCreate(ClassBase):
    """Class creation schema."""

    pass


class ClassResponse(ClassBase):
    """Class response schema."""

    id: int
    created_at: datetime
    file_count: Optional[int] = 0

    class Config:
        from_attributes = True
