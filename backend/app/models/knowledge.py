from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON, TIMESTAMP, Column, Index, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True, index=True)
    source_table = Column(String(50), nullable=False, index=True)
    source_id = Column(Integer, nullable=False, index=True)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(Vector(768))  # multilingual-e5-base dimension
    chunk_metadata = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (Index("idx_chunks_source", "source_table", "source_id"),)
