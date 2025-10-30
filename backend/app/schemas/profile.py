from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date
from enum import Enum

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
    job_title: Optional[str] = None
    location: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None
    summary: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class ProfileBasicsResponse(ProfileBasicsBase):
    id: int

    class Config:
        from_attributes = True

class WorkExperienceBase(BaseModel):
    company_name: str
    position: str
    location: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None
    achievements: Optional[List[str]] = []
    technologies: Optional[List[str]] = []
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
    proficiency_level: Optional[ProficiencyLevel] = None
    years_of_experience: Optional[float] = None
    order_index: int = 0

class SkillResponse(SkillBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class SkillCategoryResponse(SkillCategoryBase):
    id: int
    skills: List[SkillResponse] = []

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str
    short_description: Optional[str] = None
    full_description: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    technologies: Optional[List[str]] = []
    project_url: Optional[str] = None
    github_url: Optional[str] = None
    image_url: Optional[str] = None
    highlights: Optional[List[str]] = []
    order_index: int = 0
    is_featured: bool = False

class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True

class EducationBase(BaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0

class EducationResponse(EducationBase):
    id: int

    class Config:
        from_attributes = True

class LanguageBase(BaseModel):
    name: str
    proficiency: Optional[LanguageProficiency] = None
    order_index: int = 0

class LanguageResponse(LanguageBase):
    id: int

    class Config:
        from_attributes = True

class CertificationBase(BaseModel):
    name: str
    issuing_organization: Optional[str] = None
    issue_date: Optional[date] = None
    expiry_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    order_index: int = 0

class CertificationResponse(CertificationBase):
    id: int

    class Config:
        from_attributes = True

# Complete profile response
class CompleteProfileResponse(BaseModel):
    basics: Optional[ProfileBasicsResponse] = None
    experience: List[WorkExperienceResponse] = []
    skills: List[SkillCategoryResponse] = []
    projects: List[ProjectResponse] = []
    education: List[EducationResponse] = []
    languages: List[LanguageResponse] = []
    certifications: List[CertificationResponse] = []

# Admin schemas for updates
class ProfileUpdateRequest(BaseModel):
    section: str  # "basics", "experience", "skills", etc.
    action: str   # "create", "update", "delete"
    id: Optional[int] = None
    data: Optional[dict] = None
