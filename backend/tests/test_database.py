import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import Base, engine, AsyncSessionLocal, get_db
from app.models.profile import ProfileBasics, SkillCategory, Skill
import asyncio


@pytest.mark.integration
def test_database_connection_sync():
    """Test synchronous database connection"""
    try:
        sync_engine = create_engine(settings.database_url_sync)
        with sync_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
        sync_engine.dispose()
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_database_connection_async():
    """Test asynchronous database connection"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
def test_pgvector_extension():
    """Test that pgvector extension is available"""
    try:
        sync_engine = create_engine(settings.database_url_sync)
        with sync_engine.connect() as conn:
            result = conn.execute(text(
                "SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'vector')"
            ))
            has_pgvector = result.scalar()
            assert has_pgvector, "pgvector extension not installed"
        sync_engine.dispose()
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_db_dependency():
    """Test FastAPI database dependency"""
    try:
        async for session in get_db():
            assert session is not None
            # Test simple query
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_tables():
    """Test creating all tables"""
    try:
        async with engine.begin() as conn:
            # Drop all tables first (for clean test)
            await conn.run_sync(Base.metadata.drop_all)
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)

            # Verify tables exist
            result = await conn.execute(text(
                "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
            ))
            tables = [row[0] for row in result]

            # Check that our tables are created
            expected_tables = [
                'profile_basics', 'work_experience', 'skill_categories',
                'skills', 'projects', 'education', 'languages',
                'certifications', 'chat_sessions', 'chat_messages',
                'knowledge_chunks'
            ]

            for table in expected_tables:
                assert table in tables, f"Table {table} not created"
    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_crud_operations():
    """Test basic CRUD operations"""
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        # Test CREATE
        async with AsyncSessionLocal() as session:
            # Create profile
            profile = ProfileBasics(
                full_name="Test User",
                job_title="Software Engineer",
                email="test@example.com"
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)

            profile_id = profile.id
            assert profile_id is not None

        # Test READ
        async with AsyncSessionLocal() as session:
            from sqlalchemy import select
            result = await session.execute(
                select(ProfileBasics).where(ProfileBasics.id == profile_id)
            )
            profile = result.scalar_one()
            assert profile.full_name == "Test User"
            assert profile.email == "test@example.com"

        # Test UPDATE
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ProfileBasics).where(ProfileBasics.id == profile_id)
            )
            profile = result.scalar_one()
            profile.job_title = "Senior Software Engineer"
            await session.commit()

        # Verify update
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ProfileBasics).where(ProfileBasics.id == profile_id)
            )
            profile = result.scalar_one()
            assert profile.job_title == "Senior Software Engineer"

        # Test DELETE
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ProfileBasics).where(ProfileBasics.id == profile_id)
            )
            profile = result.scalar_one()
            await session.delete(profile)
            await session.commit()

        # Verify deletion
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ProfileBasics).where(ProfileBasics.id == profile_id)
            )
            profile = result.scalar_one_or_none()
            assert profile is None

    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_relationship_cascade():
    """Test cascade delete for relationships"""
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async with AsyncSessionLocal() as session:
            from sqlalchemy import select

            # Create category with skill
            category = SkillCategory(name="Backend")
            session.add(category)
            await session.commit()
            await session.refresh(category)

            skill = Skill(
                category_id=category.id,
                name="Python",
                proficiency_level="expert"
            )
            session.add(skill)
            await session.commit()

            category_id = category.id

            # Delete category
            await session.delete(category)
            await session.commit()

            # Verify skill is also deleted (cascade)
            result = await session.execute(
                select(Skill).where(Skill.category_id == category_id)
            )
            skills = result.scalars().all()
            assert len(skills) == 0, "Skills should be deleted with category (cascade)"

    except OperationalError as e:
        pytest.skip(f"Database not available: {e}")


@pytest.mark.integration
def test_database_url_configuration():
    """Test that database URLs are properly configured"""
    assert settings.database_url is not None
    assert settings.database_url_sync is not None
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.database_url_sync.startswith("postgresql://")

    # Ensure both URLs point to the same database
    async_parts = settings.database_url.replace("postgresql+asyncpg://", "")
    sync_parts = settings.database_url_sync.replace("postgresql://", "")

    # Compare database names (last part after /)
    async_db = async_parts.split("/")[-1]
    sync_db = sync_parts.split("/")[-1]
    assert async_db == sync_db, "Async and sync URLs must point to same database"
