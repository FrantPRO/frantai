import pytest
from datetime import date
from app.models.profile import (
    ProfileBasics, WorkExperience, Project,
    Education, Language, Certification, SkillCategory, Skill
)
from app.services.formatters import (
    format_profile_basics, format_work_experience,
    format_project, format_education, format_language,
    format_certification, format_skill_category
)

@pytest.mark.unit
def test_format_profile_basics():
    """Test formatting ProfileBasics"""
    basics = ProfileBasics(
        id=1,
        full_name="Stan Frant",
        job_title="Backend Developer",
        location="Remote",
        email="stan@example.com",
        summary="Experienced developer"
    )

    text = format_profile_basics(basics)

    assert "Stan Frant" in text
    assert "Backend Developer" in text
    assert "Remote" in text
    assert "stan@example.com" in text
    assert "Experienced developer" in text

@pytest.mark.unit
def test_format_work_experience():
    """Test formatting WorkExperience"""
    exp = WorkExperience(
        id=1,
        company_name="Test Corp",
        position="Senior Developer",
        start_date=date(2020, 1, 1),
        end_date=date(2023, 12, 31),
        is_current=False,
        description="Developed backend systems",
        achievements=["Achievement 1", "Achievement 2"],
        technologies=["Python", "Go"]
    )

    text = format_work_experience(exp)

    assert "Test Corp" in text
    assert "Senior Developer" in text
    assert "January 2020" in text
    assert "December 2023" in text
    assert "Achievement 1" in text
    assert "Python" in text
    assert "Go" in text

@pytest.mark.unit
def test_format_work_experience_current():
    """Test formatting current work experience"""
    exp = WorkExperience(
        id=1,
        company_name="Current Corp",
        position="Lead Developer",
        start_date=date(2023, 1, 1),
        is_current=True
    )

    text = format_work_experience(exp)

    assert "Present" in text
    assert "Current Corp" in text

@pytest.mark.unit
def test_format_project():
    """Test formatting Project"""
    project = Project(
        id=1,
        name="FrantAI",
        short_description="AI chat bot",
        full_description="Full stack AI application",
        role="Lead Developer",
        technologies=["FastAPI", "React"],
        highlights=["Implemented RAG", "Deployed to production"],
        project_url="https://example.com"
    )

    text = format_project(project)

    assert "FrantAI" in text
    assert "AI chat bot" in text
    assert "FastAPI" in text
    assert "Implemented RAG" in text
    assert "https://example.com" in text

@pytest.mark.unit
def test_format_skill_category():
    """Test formatting SkillCategory with skills"""
    category = SkillCategory(id=1, name="Backend")
    skills = [
        Skill(id=1, category_id=1, name="Python", proficiency_level="expert", years_of_experience=5.0),
        Skill(id=2, category_id=1, name="Go", proficiency_level="advanced", years_of_experience=3.0)
    ]

    text = format_skill_category(category, skills)

    assert "Backend" in text
    assert "Python" in text
    assert "expert" in text
    assert "5" in text or "5.0" in text
    assert "Go" in text
    assert "advanced" in text
