"""Chat schemas."""
from pydantic import BaseModel
from typing import List, Optional


class ChatMessage(BaseModel):
    """Chat message schema."""

    class_id: int
    message: str


class SourceDocument(BaseModel):
    """Source document schema."""

    filename: str
    content: str


class ChatResponse(BaseModel):
    """Chat response schema."""

    answer: str
    sources: List[SourceDocument] = []
