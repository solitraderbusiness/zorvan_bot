"""File schemas."""
from pydantic import BaseModel
from datetime import datetime


class FileResponse(BaseModel):
    """File response schema."""

    id: int
    class_id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    is_processed: bool
    created_at: datetime

    class Config:
        from_attributes = True
