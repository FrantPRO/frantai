from datetime import date
from enum import Enum

from pydantic import BaseModel, EmailStr


# Enums
class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class LanguageProficiency(str, Enum):
    NATIVE = "native"
    FLUENT = "fluent"
    PROFESSIONAL = "professional"
    INTERMEDIATE = "intermediate"
    BASIC = "basic"


# Base schemas
class ProfileBasicsBase(BaseModel):
    full_name: str
    job_title: str | None = None
    location: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    website_url: str | None = None
    summary: str | None = None
    bio: str | None = None
    avatar_url: str | None = None


class ProfileBasicsResponse(ProfileBasicsBase):
    id: int

    class Config:
        from_attributes = True


class WorkExperienceBase(BaseModel):
    company_name: str
    position: str
    location: str | None = None
    start_date: date
    end_date: date | None = None
    is_current: bool = False
    description: str | None = None
    achievements: list[str] | None = []
    technologies: list[str] | None = []
    order_index: int = 0


class WorkExperienceResponse(WorkExperienceBase):
    id: int

    class Config:
        from_attributes = True


class SkillCategoryBase(BaseModel):
    name: str
    order_index: int = 0


class SkillBase(BaseModel):
    name: str
    proficiency_level: ProficiencyLevel | None = None
    years_of_experience: float | None = None
    order_index: int = 0


class SkillResponse(SkillBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True


class SkillCategoryResponse(SkillCategoryBase):
    id: int
    skills: list[SkillResponse] = []

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    short_description: str | None = None
    full_description: str | None = None
    role: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    technologies: list[str] | None = []
    project_url: str | None = None
    github_url: str | None = None
    image_url: str | None = None
    highlights: list[str] | None = []
    order_index: int = 0
    is_featured: bool = False


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class EducationBase(BaseModel):
    institution: str
    degree: str | None = None
    field_of_study: str | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    grade: str | None = None
    description: str | None = None
    order_index: int = 0


class EducationResponse(EducationBase):
    id: int

    class Config:
        from_attributes = True


class LanguageBase(BaseModel):
    name: str
    proficiency: LanguageProficiency | None = None
    order_index: int = 0


class LanguageResponse(LanguageBase):
    id: int

    class Config:
        from_attributes = True


class CertificationBase(BaseModel):
    name: str
    issuing_organization: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    credential_id: str | None = None
    credential_url: str | None = None
    order_index: int = 0


class CertificationResponse(CertificationBase):
    id: int

    class Config:
        from_attributes = True


# Complete profile response
class CompleteProfileResponse(BaseModel):
    basics: ProfileBasicsResponse | None = None
    experience: list[WorkExperienceResponse] = []
    skills: list[SkillCategoryResponse] = []
    projects: list[ProjectResponse] = []
    education: list[EducationResponse] = []
    languages: list[LanguageResponse] = []
    certifications: list[CertificationResponse] = []


# Admin schemas for updates
class ProfileUpdateRequest(BaseModel):
    section: str  # "basics", "experience", "skills", etc.
    action: str  # "create", "update", "delete"
    id: int | None = None
    data: dict | None = None
