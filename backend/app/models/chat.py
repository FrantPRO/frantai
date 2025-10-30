from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    JSON,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from app.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_message_at = Column(TIMESTAMP, server_default=func.now())
    last_message_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )
    message_count = Column(Integer, default=0)
    ip_hash = Column(String(64))

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True,
    )
    role = Column(String(20), nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    retrieved_chunks = Column(JSON)  # List of integers
    language_detected = Column(String(10))
    response_time_ms = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)

    session = relationship("ChatSession", back_populates="messages")
