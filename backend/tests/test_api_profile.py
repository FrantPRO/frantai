import pytest
from httpx import AsyncClient
from datetime import date
from app.models.profile import (
    ProfileBasics, WorkExperience, SkillCategory,
    Skill, Project, Education, Language, Certification
)

@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_empty_profile(client: AsyncClient):
    """Test getting profile when database is empty"""
    response = await client.get("/api/v1/profile")
    assert response.status_code == 200
    data = response.json()
    assert data["basics"] is None
    assert data["experience"] == []
    assert data["skills"] == []

@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_complete_profile(client: AsyncClient, db_session):
    """Test getting complete profile with all sections"""
    # Create test data
    basics = ProfileBasics(
        full_name="Stan Frant",
        job_title="Backend Developer",
        email="test@example.com"
    )
    db_session.add(basics)

    exp = WorkExperience(
        company_name="Test Corp",
        position="Senior Developer",
        start_date=date(2020, 1, 1),
        is_current=True
    )
    db_session.add(exp)

    category = SkillCategory(name="Backend")
    db_session.add(category)
    await db_session.commit()

    skill = Skill(
        category_id=category.id,
        name="Python",
        proficiency_level="expert"
    )
    db_session.add(skill)

    await db_session.commit()

    # Get profile
    response = await client.get("/api/v1/profile")
    assert response.status_code == 200

    data = response.json()
    assert data["basics"]["full_name"] == "Stan Frant"
    assert len(data["experience"]) == 1
    assert data["experience"][0]["company_name"] == "Test Corp"
    assert len(data["skills"]) == 1
    assert data["skills"][0]["name"] == "Backend"
    assert len(data["skills"][0]["skills"]) == 1

@pytest.mark.unit
@pytest.mark.asyncio
async def test_admin_create_experience(client: AsyncClient, db_session):
    """Test creating work experience via admin API"""
    response = await client.put(
        "/api/v1/admin/profile",
        json={
            "section": "experience",
            "action": "create",
            "data": {
                "company_name": "New Company",
                "position": "Lead Developer",
                "start_date": "2021-01-01",
                "is_current": True
            }
        },
        headers={"X-Admin-Token": "dev-admin-token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "id" in data

@pytest.mark.unit
@pytest.mark.asyncio
async def test_admin_update_experience(client: AsyncClient, db_session):
    """Test updating work experience"""
    # Create
    exp = WorkExperience(
        company_name="Old Company",
        position="Developer",
        start_date=date(2020, 1, 1)
    )
    db_session.add(exp)
    await db_session.commit()

    # Update
    response = await client.put(
        "/api/v1/admin/profile",
        json={
            "section": "experience",
            "action": "update",
            "id": exp.id,
            "data": {"company_name": "Updated Company"}
        },
        headers={"X-Admin-Token": "dev-admin-token"}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.unit
@pytest.mark.asyncio
async def test_admin_delete_experience(client: AsyncClient, db_session):
    """Test deleting work experience"""
    exp = WorkExperience(
        company_name="Test Company",
        position="Developer",
        start_date=date(2020, 1, 1)
    )
    db_session.add(exp)
    await db_session.commit()

    response = await client.put(
        "/api/v1/admin/profile",
        json={
            "section": "experience",
            "action": "delete",
            "id": exp.id
        },
        headers={"X-Admin-Token": "dev-admin-token"}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True

@pytest.mark.unit
@pytest.mark.asyncio
async def test_admin_unauthorized(client: AsyncClient):
    """Test admin endpoint without token"""
    response = await client.put(
        "/api/v1/admin/profile",
        json={"section": "experience", "action": "create", "data": {}}
    )
    assert response.status_code == 401

@pytest.mark.unit
@pytest.mark.asyncio
async def test_admin_invalid_token(client: AsyncClient):
    """Test admin endpoint with invalid token"""
    response = await client.put(
        "/api/v1/admin/profile",
        json={"section": "experience", "action": "create", "data": {}},
        headers={"X-Admin-Token": "wrong-token"}
    )
    assert response.status_code == 403

@pytest.mark.unit
@pytest.mark.asyncio
async def test_profile_ordering(client: AsyncClient, db_session):
    """Test that items are returned in correct order"""
    # Create multiple experiences with different order_index
    exp1 = WorkExperience(
        company_name="Company A",
        position="Dev",
        start_date=date(2020, 1, 1),
        order_index=2
    )
    exp2 = WorkExperience(
        company_name="Company B",
        position="Dev",
        start_date=date(2021, 1, 1),
        order_index=1
    )
    db_session.add_all([exp1, exp2])
    await db_session.commit()

    response = await client.get("/api/v1/profile")
    data = response.json()

    # Should be ordered by order_index
    assert data["experience"][0]["company_name"] == "Company B"
    assert data["experience"][1]["company_name"] == "Company A"

@pytest.mark.unit
@pytest.mark.asyncio
async def test_delete_section_item(client: AsyncClient, db_session):
    """Test deleting item via direct delete endpoint"""
    exp = WorkExperience(
        company_name="Delete Me",
        position="Developer",
        start_date=date(2020, 1, 1)
    )
    db_session.add(exp)
    await db_session.commit()

    response = await client.delete(
        f"/api/v1/admin/profile/section/experience/{exp.id}",
        headers={"X-Admin-Token": "dev-admin-token"}
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
