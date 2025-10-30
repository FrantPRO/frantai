"""
Pydantic schemas for chat endpoints.
"""

from uuid import UUID

from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    """Request schema for chat message"""

    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's question or message",
    )
    session_id: UUID | None = Field(
        None, description="Session ID (will be created if not provided)"
    )


class ChatMessageResponse(BaseModel):
    """Response schema for chat message (non-streaming)"""

    response: str
    session_id: UUID
    chunks_used: int


class SessionResponse(BaseModel):
    """Response schema for session info"""

    session_id: UUID
    message_count: int
    first_message_at: str
    last_message_at: str
