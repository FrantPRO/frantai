import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.indexing import IndexingService
from app.models.profile import ProfileBasics, WorkExperience, Project, SkillCategory, Skill

@pytest.mark.unit
@pytest.mark.asyncio
async def test_indexing_service_init():
    """Test IndexingService initialization"""
    mock_db = AsyncMock(spec=AsyncSession)

    with patch('app.services.indexing.get_embedding_service'):
        service = IndexingService(mock_db)
        assert service.db == mock_db

@pytest.mark.unit
@pytest.mark.asyncio
async def test_index_profile_basics():
    """Test indexing ProfileBasics"""
    mock_db = AsyncMock(spec=AsyncSession)
    mock_embedding_service = Mock()
    mock_embedding_service.create_passage_embedding.return_value = [0.1, 0.2, 0.3]

    # Mock database query
    mock_result = Mock()
    mock_basics = ProfileBasics(
        id=1,
        full_name="Stan Frant",
        job_title="Backend Developer",
        summary="Test summary"
    )
    mock_result.scalar_one_or_none.return_value = mock_basics
    mock_db.execute.return_value = mock_result

    with patch('app.services.indexing.get_embedding_service', return_value=mock_embedding_service):
        service = IndexingService(mock_db)
        chunks_created = await service.index_profile_basics(1)

        assert chunks_created > 0
        assert mock_db.add.called
        assert mock_db.commit.called

@pytest.mark.unit
@pytest.mark.asyncio
async def test_index_work_experience():
    """Test indexing WorkExperience"""
    mock_db = AsyncMock(spec=AsyncSession)
    mock_embedding_service = Mock()
    mock_embedding_service.create_passage_embedding.return_value = [0.1, 0.2]

    mock_result = Mock()
    mock_exp = WorkExperience(
        id=1,
        company_name="Test Corp",
        position="Developer",
        start_date=date(2020, 1, 1),
        is_current=True,
        description="Long description " * 100  # Force chunking
    )
    mock_result.scalar_one_or_none.return_value = mock_exp
    mock_db.execute.return_value = mock_result

    with patch('app.services.indexing.get_embedding_service', return_value=mock_embedding_service):
        service = IndexingService(mock_db)
        chunks_created = await service.index_work_experience(1)

        # Should create multiple chunks for long text
        assert chunks_created >= 1

@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_chunks():
    """Test deleting old chunks"""
    mock_db = AsyncMock(spec=AsyncSession)

    with patch('app.services.indexing.get_embedding_service'):
        service = IndexingService(mock_db)
        await service._delete_chunks("work_experience", 1)

        assert mock_db.execute.called
