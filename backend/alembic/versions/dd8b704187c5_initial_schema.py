"""Initial schema

Revision ID: dd8b704187c5
Revises:
Create Date: 2025-10-29 21:28:26.644353

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "dd8b704187c5"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Profile basics
    op.create_table(
        "profile_basics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("job_title", sa.String(length=200), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("email", sa.String(length=200), nullable=True),
        sa.Column("phone", sa.String(length=50), nullable=True),
        sa.Column("linkedin_url", sa.String(length=300), nullable=True),
        sa.Column("github_url", sa.String(length=300), nullable=True),
        sa.Column("website_url", sa.String(length=300), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_url", sa.String(length=300), nullable=True),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_profile_basics_id"), "profile_basics", ["id"], unique=False
    )

    # Work experience
    op.create_table(
        "work_experience",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("company_name", sa.String(length=200), nullable=False),
        sa.Column("position", sa.String(length=200), nullable=False),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("achievements", postgresql.JSONB(), nullable=True),
        sa.Column("technologies", postgresql.JSONB(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_work_experience_id"), "work_experience", ["id"], unique=False
    )

    # Skill categories
    op.create_table(
        "skill_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(
        op.f("ix_skill_categories_id"), "skill_categories", ["id"], unique=False
    )

    # Skills
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("proficiency_level", sa.String(length=50), nullable=True),
        sa.Column("years_of_experience", sa.Float(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"], ["skill_categories.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_skills_id"), "skills", ["id"], unique=False)

    # Projects
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("full_description", sa.Text(), nullable=True),
        sa.Column("role", sa.String(length=200), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("technologies", postgresql.JSONB(), nullable=True),
        sa.Column("project_url", sa.String(length=300), nullable=True),
        sa.Column("github_url", sa.String(300), nullable=True),
        sa.Column("image_url", sa.String(length=300), nullable=True),
        sa.Column("highlights", postgresql.JSONB(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=True),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)

    # Education
    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("institution", sa.String(length=200), nullable=False),
        sa.Column("degree", sa.String(length=200), nullable=True),
        sa.Column("field_of_study", sa.String(length=200), nullable=True),
        sa.Column("location", sa.String(length=200), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("grade", sa.String(length=50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_education_id"), "education", ["id"], unique=False)

    # Languages
    op.create_table(
        "languages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("proficiency", sa.String(length=50), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_languages_id"), "languages", ["id"], unique=False)

    # Certifications
    op.create_table(
        "certifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("issuing_organization", sa.String(length=200), nullable=True),
        sa.Column("issue_date", sa.Date(), nullable=True),
        sa.Column("expiry_date", sa.Date(), nullable=True),
        sa.Column("credential_id", sa.String(length=200), nullable=True),
        sa.Column("credential_url", sa.String(length=300), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_certifications_id"), "certifications", ["id"], unique=False
    )

    # Chat sessions
    op.create_table(
        "chat_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "first_message_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "last_message_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("message_count", sa.Integer(), nullable=True),
        sa.Column("ip_hash", sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Chat messages
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("retrieved_chunks", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("language_detected", sa.String(length=10), nullable=True),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["session_id"], ["chat_sessions.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_chat_messages_created_at"),
        "chat_messages",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_chat_messages_id"), "chat_messages", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_chat_messages_session_id"),
        "chat_messages",
        ["session_id"],
        unique=False,
    )

    # Knowledge chunks
    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_table", sa.String(length=50), nullable=False),
        sa.Column("source_id", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(768), nullable=True),
        sa.Column(
            "chunk_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_chunks_source",
        "knowledge_chunks",
        ["source_table", "source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_chunks_id"), "knowledge_chunks", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_knowledge_chunks_source_id"),
        "knowledge_chunks",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_chunks_source_table"),
        "knowledge_chunks",
        ["source_table"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_knowledge_chunks_source_table"), table_name="knowledge_chunks"
    )
    op.drop_index(
        op.f("ix_knowledge_chunks_source_id"), table_name="knowledge_chunks"
    )
    op.drop_index(op.f("ix_knowledge_chunks_id"), table_name="knowledge_chunks")
    op.drop_index("idx_chunks_source", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")

    op.drop_index(
        op.f("ix_chat_messages_session_id"), table_name="chat_messages"
    )
    op.drop_index(op.f("ix_chat_messages_id"), table_name="chat_messages")
    op.drop_index(
        op.f("ix_chat_messages_created_at"), table_name="chat_messages"
    )
    op.drop_table("chat_messages")

    op.drop_table("chat_sessions")

    op.drop_index(op.f("ix_certifications_id"), table_name="certifications")
    op.drop_table("certifications")

    op.drop_index(op.f("ix_languages_id"), table_name="languages")
    op.drop_table("languages")

    op.drop_index(op.f("ix_education_id"), table_name="education")
    op.drop_table("education")

    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")

    op.drop_index(op.f("ix_skills_id"), table_name="skills")
    op.drop_table("skills")

    op.drop_index(op.f("ix_skill_categories_id"), table_name="skill_categories")
    op.drop_table("skill_categories")

    op.drop_index(op.f("ix_work_experience_id"), table_name="work_experience")
    op.drop_table("work_experience")

    op.drop_index(op.f("ix_profile_basics_id"), table_name="profile_basics")
    op.drop_table("profile_basics")
