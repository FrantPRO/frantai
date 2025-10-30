from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, date
from app.api.deps import get_db, verify_admin_access
from app.schemas.profile import (
    ProfileUpdateRequest,
    CompleteProfileResponse
)
from app.models.profile import (
    ProfileBasics,
    WorkExperience,
    SkillCategory,
    Skill,
    Project,
    Education,
    Language,
    Certification
)

router = APIRouter()

def convert_dates_in_dict(data: dict) -> dict:
    """Convert date strings to date objects in a dictionary"""
    result = {}
    for key, value in data.items():
        if value and isinstance(value, str):
            # Try to parse as date
            if '_date' in key or key in ['start_date', 'end_date', 'issue_date', 'expiry_date']:
                try:
                    result[key] = datetime.fromisoformat(value).date()
                except (ValueError, AttributeError):
                    result[key] = value
            else:
                result[key] = value
        else:
            result[key] = value
    return result

# Mapping section names to models
SECTION_MODELS = {
    "basics": ProfileBasics,
    "experience": WorkExperience,
    "skill_categories": SkillCategory,
    "skills": Skill,
    "projects": Project,
    "education": Education,
    "languages": Language,
    "certifications": Certification,
}

@router.get("/profile", response_model=CompleteProfileResponse)
async def get_admin_profile(
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    """Get complete profile (admin version - same as public for now)"""
    # Import here to avoid circular dependency
    from app.api.v1.profile import get_complete_profile
    return await get_complete_profile(db)

@router.put("/profile")
async def update_profile_section(
    request: ProfileUpdateRequest,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    """
    Update profile section.
    Actions: create, update, delete
    """
    model = SECTION_MODELS.get(request.section)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid section: {request.section}"
        )

    if request.action == "create":
        # Create new record
        if not request.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data required for create action"
            )
        # Convert date strings to date objects
        converted_data = convert_dates_in_dict(request.data)
        instance = model(**converted_data)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)

        return {
            "success": True,
            "message": f"{request.section} created",
            "id": instance.id
        }

    elif request.action == "update":
        # Update existing record
        if not request.id or not request.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID and data required for update action"
            )

        result = await db.execute(select(model).where(model.id == request.id))
        instance = result.scalar_one_or_none()

        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{request.section} with id {request.id} not found"
            )

        # Convert date strings to date objects
        converted_data = convert_dates_in_dict(request.data)
        for key, value in converted_data.items():
            setattr(instance, key, value)

        await db.commit()
        await db.refresh(instance)

        return {
            "success": True,
            "message": f"{request.section} updated",
            "id": instance.id
        }

    elif request.action == "delete":
        # Delete record
        if not request.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ID required for delete action"
            )

        result = await db.execute(
            delete(model).where(model.id == request.id)
        )

        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{request.section} with id {request.id} not found"
            )

        await db.commit()

        return {
            "success": True,
            "message": f"{request.section} deleted"
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid action: {request.action}"
        )

@router.delete("/profile/section/{table}/{id}")
async def delete_section_item(
    table: str,
    id: int,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    """Delete specific item from any table"""
    model = SECTION_MODELS.get(table)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid table: {table}"
        )

    result = await db.execute(delete(model).where(model.id == id))

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {id} not found in {table}"
        )

    await db.commit()

    return {"success": True, "message": f"Item deleted from {table}"}

@router.post("/reindex")
async def reindex_knowledge_base(
    tables: list[str] = None,
    db: AsyncSession = Depends(get_db),
    _: bool = Depends(verify_admin_access)
):
    """
    Reindex all or specific profile data into knowledge chunks.

    Args:
        tables: Optional list of tables to reindex. If None, reindex all.
                Supported: ["profile_basics", "work_experience", "projects",
                           "skill_categories", "education"]
    """
    import time
    from app.services.indexing import IndexingService

    start_time = time.time()

    indexing_service = IndexingService(db)

    if not tables:
        # Reindex everything
        stats = await indexing_service.index_all()
    else:
        # Reindex specific tables
        stats = {}

        if "profile_basics" in tables:
            result = await db.execute(select(ProfileBasics))
            basics = result.scalar_one_or_none()
            if basics:
                stats["profile_basics"] = await indexing_service.index_profile_basics(basics.id)

        if "work_experience" in tables:
            result = await db.execute(select(WorkExperience))
            experiences = result.scalars().all()
            chunks = 0
            for exp in experiences:
                chunks += await indexing_service.index_work_experience(exp.id)
            stats["work_experience"] = chunks

        if "projects" in tables:
            result = await db.execute(select(Project))
            projects = result.scalars().all()
            chunks = 0
            for project in projects:
                chunks += await indexing_service.index_project(project.id)
            stats["projects"] = chunks

        if "skill_categories" in tables:
            result = await db.execute(select(SkillCategory))
            categories = result.scalars().all()
            chunks = 0
            for category in categories:
                chunks += await indexing_service.index_skill_category(category.id)
            stats["skill_categories"] = chunks

        if "education" in tables:
            result = await db.execute(select(Education))
            educations = result.scalars().all()
            chunks = 0
            for edu in educations:
                chunks += await indexing_service.index_education(edu.id)
            stats["education"] = chunks

        stats["total_chunks"] = sum(stats.values())

    duration_ms = int((time.time() - start_time) * 1000)

    return {
        "success": True,
        "stats": stats,
        "duration_ms": duration_ms
    }
