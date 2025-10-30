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
