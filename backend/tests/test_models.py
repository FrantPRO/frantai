import pytest
from datetime import date, datetime
from uuid import uuid4
from app.database import Base
from app.models.profile import (
    ProfileBasics, WorkExperience, SkillCategory,
    Skill, Project, Education, Language, Certification
)
from app.models.chat import ChatSession, ChatMessage
from app.models.knowledge import KnowledgeChunk


@pytest.mark.unit
def test_models_import():
    """Test that all models can be imported successfully"""
    assert ProfileBasics is not None
    assert WorkExperience is not None
    assert SkillCategory is not None
    assert Skill is not None
    assert Project is not None
    assert Education is not None
    assert Language is not None
    assert Certification is not None
    assert ChatSession is not None
    assert ChatMessage is not None
    assert KnowledgeChunk is not None

@pytest.mark.unit
def test_profile_basics_attributes():
    """Test ProfileBasics model attributes"""
    assert hasattr(ProfileBasics, 'full_name')
    assert hasattr(ProfileBasics, 'job_title')
    assert hasattr(ProfileBasics, 'email')
    assert hasattr(ProfileBasics, 'summary')
    assert hasattr(ProfileBasics, 'bio')
    assert hasattr(ProfileBasics, 'updated_at')

@pytest.mark.unit
def test_work_experience_attributes():
    """Test WorkExperience model attributes"""
    assert hasattr(WorkExperience, 'company_name')
    assert hasattr(WorkExperience, 'position')
    assert hasattr(WorkExperience, 'start_date')
    assert hasattr(WorkExperience, 'end_date')
    assert hasattr(WorkExperience, 'is_current')
    assert hasattr(WorkExperience, 'technologies')
    assert hasattr(WorkExperience, 'achievements')

@pytest.mark.unit
def test_skill_category_relationship():
    """Test SkillCategory and Skill relationship"""
    assert hasattr(SkillCategory, 'skills')
    assert hasattr(Skill, 'category')
    assert hasattr(Skill, 'category_id')

@pytest.mark.unit
def test_project_attributes():
    """Test Project model attributes"""
    assert hasattr(Project, 'name')
    assert hasattr(Project, 'short_description')
    assert hasattr(Project, 'technologies')
    assert hasattr(Project, 'is_featured')
    assert hasattr(Project, 'github_url')

@pytest.mark.unit
def test_chat_session_relationship():
    """Test ChatSession and ChatMessage relationship"""
    assert hasattr(ChatSession, 'messages')
    assert hasattr(ChatMessage, 'session')
    assert hasattr(ChatMessage, 'session_id')
    assert hasattr(ChatMessage, 'role')
    assert hasattr(ChatMessage, 'content')

@pytest.mark.unit
def test_knowledge_chunk_attributes():
    """Test KnowledgeChunk model attributes"""
    assert hasattr(KnowledgeChunk, 'source_table')
    assert hasattr(KnowledgeChunk, 'source_id')
    assert hasattr(KnowledgeChunk, 'chunk_text')
    assert hasattr(KnowledgeChunk, 'embedding')
    assert hasattr(KnowledgeChunk, 'chunk_metadata')

@pytest.mark.unit
def test_education_attributes():
    """Test Education model attributes"""
    assert hasattr(Education, 'institution')
    assert hasattr(Education, 'degree')
    assert hasattr(Education, 'field_of_study')

@pytest.mark.unit
def test_language_attributes():
    """Test Language model attributes"""
    assert hasattr(Language, 'name')
    assert hasattr(Language, 'proficiency')

@pytest.mark.unit
def test_certification_attributes():
    """Test Certification model attributes"""
    assert hasattr(Certification, 'name')
    assert hasattr(Certification, 'issuing_organization')
    assert hasattr(Certification, 'credential_url')
