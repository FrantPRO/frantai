from sqlalchemy import (
    JSON,
    TIMESTAMP,
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ProfileBasics(Base):
    __tablename__ = "profile_basics"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    job_title = Column(String(200))
    location = Column(String(200))
    email = Column(String(200))
    phone = Column(String(50))
    linkedin_url = Column(String(300))
    github_url = Column(String(300))
    website_url = Column(String(300))
    summary = Column(Text)
    bio = Column(Text)
    avatar_url = Column(String(300))
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class WorkExperience(Base):
    __tablename__ = "work_experience"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    location = Column(String(200))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    description = Column(Text)
    achievements = Column(JSON)  # List of strings
    technologies = Column(JSON)  # List of strings
    order_index = Column(Integer, default=0)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class SkillCategory(Base):
    __tablename__ = "skill_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    order_index = Column(Integer, default=0)

    skills = relationship(
        "Skill", back_populates="category", cascade="all, delete-orphan"
    )


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(
        Integer, ForeignKey("skill_categories.id", ondelete="CASCADE")
    )
    name = Column(String(100), nullable=False)
    proficiency_level = Column(
        String(50)
    )  # beginner, intermediate, advanced, expert
    years_of_experience = Column(Float)
    order_index = Column(Integer, default=0)

    category = relationship("SkillCategory", back_populates="skills")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    short_description = Column(Text)
    full_description = Column(Text)
    role = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    technologies = Column(JSON)  # List of strings
    project_url = Column(String(300))
    github_url = Column(String(300))
    image_url = Column(String(300))
    highlights = Column(JSON)  # List of strings
    order_index = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    updated_at = Column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(200), nullable=False)
    degree = Column(String(200))
    field_of_study = Column(String(200))
    location = Column(String(200))
    start_date = Column(Date)
    end_date = Column(Date)
    grade = Column(String(50))
    description = Column(Text)
    order_index = Column(Integer, default=0)


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    proficiency = Column(
        String(50)
    )  # native, fluent, professional, intermediate, basic
    order_index = Column(Integer, default=0)


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    issuing_organization = Column(String(200))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    credential_id = Column(String(200))
    credential_url = Column(String(300))
    order_index = Column(Integer, default=0)
