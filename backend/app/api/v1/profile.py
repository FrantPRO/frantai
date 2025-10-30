from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.deps import get_db
from app.schemas.profile import CompleteProfileResponse
from app.models.profile import (
    ProfileBasics,
    WorkExperience,
    SkillCategory,
    Project,
    Education,
    Language,
    Certification
)

router = APIRouter()

@router.get("", response_model=CompleteProfileResponse)
async def get_complete_profile(db: AsyncSession = Depends(get_db)):
    """
    Get complete profile with all sections.
    Public endpoint - no authentication required.
    """
    # Basics
    basics_result = await db.execute(select(ProfileBasics))
    basics = basics_result.scalar_one_or_none()

    # Experience (ordered)
    exp_result = await db.execute(
        select(WorkExperience).order_by(WorkExperience.order_index)
    )
    experience = exp_result.scalars().all()

    # Skills with categories (ordered, with relationship)
    skills_result = await db.execute(
        select(SkillCategory)
        .options(selectinload(SkillCategory.skills))
        .order_by(SkillCategory.order_index)
    )
    skills = skills_result.scalars().all()

    # Projects (ordered, featured first)
    projects_result = await db.execute(
        select(Project)
        .order_by(Project.is_featured.desc(), Project.order_index)
    )
    projects = projects_result.scalars().all()

    # Education (ordered)
    edu_result = await db.execute(
        select(Education).order_by(Education.order_index)
    )
    education = edu_result.scalars().all()

    # Languages (ordered)
    lang_result = await db.execute(
        select(Language).order_by(Language.order_index)
    )
    languages = lang_result.scalars().all()

    # Certifications (ordered)
    cert_result = await db.execute(
        select(Certification).order_by(Certification.order_index)
    )
    certifications = cert_result.scalars().all()

    return CompleteProfileResponse(
        basics=basics,
        experience=experience,
        skills=skills,
        projects=projects,
        education=education,
        languages=languages,
        certifications=certifications
    )
