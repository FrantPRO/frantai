"""
Formatters for converting database models to text chunks.
Used by indexing service to create searchable content.
"""
from typing import List
from app.models.profile import (
    ProfileBasics, WorkExperience, Project,
    Education, Language, Certification, Skill, SkillCategory
)

def format_profile_basics(basics: ProfileBasics) -> str:
    """Format ProfileBasics into searchable text"""
    parts = []

    parts.append(f"Name: {basics.full_name}")

    if basics.job_title:
        parts.append(f"Job Title: {basics.job_title}")

    if basics.location:
        parts.append(f"Location: {basics.location}")

    if basics.summary:
        parts.append(f"\nProfessional Summary:\n{basics.summary}")

    if basics.bio:
        parts.append(f"\nBiography:\n{basics.bio}")

    # Contact info
    contact_parts = []
    if basics.email:
        contact_parts.append(f"Email: {basics.email}")
    if basics.phone:
        contact_parts.append(f"Phone: {basics.phone}")
    if basics.linkedin_url:
        contact_parts.append(f"LinkedIn: {basics.linkedin_url}")
    if basics.github_url:
        contact_parts.append(f"GitHub: {basics.github_url}")

    if contact_parts:
        parts.append("\nContact Information:\n" + "\n".join(contact_parts))

    return "\n".join(parts)

def format_work_experience(exp: WorkExperience) -> str:
    """Format WorkExperience into searchable text"""
    parts = []

    # Header
    parts.append(f"Position: {exp.position} at {exp.company_name}")

    # Period
    end_date = "Present" if exp.is_current else exp.end_date.strftime("%B %Y") if exp.end_date else "Unknown"
    start_date = exp.start_date.strftime("%B %Y")
    parts.append(f"Period: {start_date} - {end_date}")

    if exp.location:
        parts.append(f"Location: {exp.location}")

    # Description
    if exp.description:
        parts.append(f"\nDescription:\n{exp.description}")

    # Achievements
    if exp.achievements:
        parts.append("\nKey Achievements:")
        for achievement in exp.achievements:
            parts.append(f"- {achievement}")

    # Technologies
    if exp.technologies:
        parts.append(f"\nTechnologies used: {', '.join(exp.technologies)}")

    return "\n".join(parts)

def format_project(project: Project) -> str:
    """Format Project into searchable text"""
    parts = []

    parts.append(f"Project: {project.name}")

    if project.role:
        parts.append(f"Role: {project.role}")

    if project.short_description:
        parts.append(f"\n{project.short_description}")

    if project.full_description:
        parts.append(f"\nDetailed Description:\n{project.full_description}")

    # Highlights
    if project.highlights:
        parts.append("\nKey Highlights:")
        for highlight in project.highlights:
            parts.append(f"- {highlight}")

    # Technologies
    if project.technologies:
        parts.append(f"\nTechnologies: {', '.join(project.technologies)}")

    # URLs
    if project.project_url:
        parts.append(f"\nProject URL: {project.project_url}")
    if project.github_url:
        parts.append(f"GitHub: {project.github_url}")

    return "\n".join(parts)

def format_education(edu: Education) -> str:
    """Format Education into searchable text"""
    parts = []

    parts.append(f"Education: {edu.institution}")

    if edu.degree:
        parts.append(f"Degree: {edu.degree}")

    if edu.field_of_study:
        parts.append(f"Field of Study: {edu.field_of_study}")

    if edu.location:
        parts.append(f"Location: {edu.location}")

    if edu.start_date and edu.end_date:
        parts.append(f"Period: {edu.start_date.year} - {edu.end_date.year}")

    if edu.grade:
        parts.append(f"Grade: {edu.grade}")

    if edu.description:
        parts.append(f"\n{edu.description}")

    return "\n".join(parts)

def format_language(lang: Language) -> str:
    """Format Language into searchable text"""
    text = f"Language: {lang.name}"
    if lang.proficiency:
        text += f" (Proficiency: {lang.proficiency})"
    return text

def format_certification(cert: Certification) -> str:
    """Format Certification into searchable text"""
    parts = []

    parts.append(f"Certification: {cert.name}")

    if cert.issuing_organization:
        parts.append(f"Issued by: {cert.issuing_organization}")

    if cert.issue_date:
        parts.append(f"Issue Date: {cert.issue_date.strftime('%B %Y')}")

    if cert.expiry_date:
        parts.append(f"Expires: {cert.expiry_date.strftime('%B %Y')}")

    if cert.credential_url:
        parts.append(f"Credential URL: {cert.credential_url}")

    return "\n".join(parts)

def format_skill_category(category: SkillCategory, skills: List[Skill]) -> str:
    """Format SkillCategory with skills into searchable text"""
    parts = []

    parts.append(f"Skill Category: {category.name}")
    parts.append("\nSkills:")

    for skill in skills:
        skill_text = f"- {skill.name}"
        if skill.proficiency_level:
            skill_text += f" ({skill.proficiency_level})"
        if skill.years_of_experience:
            skill_text += f" - {skill.years_of_experience} years of experience"
        parts.append(skill_text)

    return "\n".join(parts)
