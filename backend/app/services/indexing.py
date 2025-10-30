"""
Indexing service for creating and managing knowledge chunks.
Automatically converts profile data into searchable embeddings.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
import logging

from app.models.profile import (
    ProfileBasics, WorkExperience, SkillCategory, Skill,
    Project, Education, Language, Certification
)
from app.models.knowledge import KnowledgeChunk
from app.services.embeddings import get_embedding_service
from app.services.text_utils import chunk_text
from app.services.formatters import (
    format_profile_basics, format_work_experience,
    format_project, format_education, format_language,
    format_certification, format_skill_category
)

logger = logging.getLogger(__name__)

class IndexingService:
    """Service for indexing profile data into knowledge chunks"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedding_service = get_embedding_service()

    async def index_profile_basics(self, basics_id: int) -> int:
        """Index ProfileBasics into knowledge chunks"""
        # Get record
        result = await self.db.execute(
            select(ProfileBasics).where(ProfileBasics.id == basics_id)
        )
        basics = result.scalar_one_or_none()

        if not basics:
            logger.warning(f"ProfileBasics with id {basics_id} not found")
            return 0

        # Delete old chunks
        await self._delete_chunks("profile_basics", basics_id)

        # Format to text
        text = format_profile_basics(basics)

        # Create chunks
        chunks = chunk_text(text, max_tokens=800, overlap=150)

        # Create embeddings and save
        chunks_created = 0
        for chunk in chunks:
            embedding = self.embedding_service.create_passage_embedding(chunk)

            knowledge_chunk = KnowledgeChunk(
                source_table="profile_basics",
                source_id=basics_id,
                chunk_text=chunk,
                embedding=embedding,
                chunk_metadata={"name": basics.full_name}
            )
            self.db.add(knowledge_chunk)
            chunks_created += 1

        await self.db.commit()
        logger.info(f"Indexed ProfileBasics {basics_id}: {chunks_created} chunks created")
        return chunks_created

    async def index_work_experience(self, exp_id: int) -> int:
        """Index WorkExperience into knowledge chunks"""
        result = await self.db.execute(
            select(WorkExperience).where(WorkExperience.id == exp_id)
        )
        exp = result.scalar_one_or_none()

        if not exp:
            logger.warning(f"WorkExperience with id {exp_id} not found")
            return 0

        await self._delete_chunks("work_experience", exp_id)

        text = format_work_experience(exp)
        chunks = chunk_text(text, max_tokens=800, overlap=150)

        chunks_created = 0
        for chunk in chunks:
            embedding = self.embedding_service.create_passage_embedding(chunk)

            knowledge_chunk = KnowledgeChunk(
                source_table="work_experience",
                source_id=exp_id,
                chunk_text=chunk,
                embedding=embedding,
                chunk_metadata={
                    "company": exp.company_name,
                    "position": exp.position
                }
            )
            self.db.add(knowledge_chunk)
            chunks_created += 1

        await self.db.commit()
        logger.info(f"Indexed WorkExperience {exp_id}: {chunks_created} chunks")
        return chunks_created

    async def index_project(self, project_id: int) -> int:
        """Index Project into knowledge chunks"""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one_or_none()

        if not project:
            return 0

        await self._delete_chunks("projects", project_id)

        text = format_project(project)
        chunks = chunk_text(text, max_tokens=800, overlap=150)

        chunks_created = 0
        for chunk in chunks:
            embedding = self.embedding_service.create_passage_embedding(chunk)

            knowledge_chunk = KnowledgeChunk(
                source_table="projects",
                source_id=project_id,
                chunk_text=chunk,
                embedding=embedding,
                chunk_metadata={"project_name": project.name}
            )
            self.db.add(knowledge_chunk)
            chunks_created += 1

        await self.db.commit()
        logger.info(f"Indexed Project {project_id}: {chunks_created} chunks")
        return chunks_created

    async def index_skill_category(self, category_id: int) -> int:
        """Index SkillCategory with all its skills"""
        result = await self.db.execute(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .where(SkillCategory.id == category_id)
        )
        category = result.scalar_one_or_none()

        if not category:
            return 0

        await self._delete_chunks("skill_categories", category_id)

        text = format_skill_category(category, category.skills)

        # Skills are usually short, one chunk is enough
        embedding = self.embedding_service.create_passage_embedding(text)

        knowledge_chunk = KnowledgeChunk(
            source_table="skill_categories",
            source_id=category_id,
            chunk_text=text,
            embedding=embedding,
            chunk_metadata={"category": category.name}
        )
        self.db.add(knowledge_chunk)

        await self.db.commit()
        logger.info(f"Indexed SkillCategory {category_id}")
        return 1

    async def index_education(self, edu_id: int) -> int:
        """Index Education into knowledge chunks"""
        result = await self.db.execute(
            select(Education).where(Education.id == edu_id)
        )
        edu = result.scalar_one_or_none()

        if not edu:
            return 0

        await self._delete_chunks("education", edu_id)

        text = format_education(edu)
        embedding = self.embedding_service.create_passage_embedding(text)

        knowledge_chunk = KnowledgeChunk(
            source_table="education",
            source_id=edu_id,
            chunk_text=text,
            embedding=embedding,
            chunk_metadata={"institution": edu.institution}
        )
        self.db.add(knowledge_chunk)

        await self.db.commit()
        logger.info(f"Indexed Education {edu_id}")
        return 1

    async def index_all(self) -> dict:
        """Index all profile data"""
        stats = {
            "profile_basics": 0,
            "work_experience": 0,
            "projects": 0,
            "skill_categories": 0,
            "education": 0,
            "total_chunks": 0
        }

        # Index basics
        result = await self.db.execute(select(ProfileBasics))
        basics = result.scalar_one_or_none()
        if basics:
            stats["profile_basics"] = await self.index_profile_basics(basics.id)

        # Index work experience
        result = await self.db.execute(select(WorkExperience))
        experiences = result.scalars().all()
        for exp in experiences:
            stats["work_experience"] += await self.index_work_experience(exp.id)

        # Index projects
        result = await self.db.execute(select(Project))
        projects = result.scalars().all()
        for project in projects:
            stats["projects"] += await self.index_project(project.id)

        # Index skill categories
        result = await self.db.execute(select(SkillCategory))
        categories = result.scalars().all()
        for category in categories:
            stats["skill_categories"] += await self.index_skill_category(category.id)

        # Index education
        result = await self.db.execute(select(Education))
        educations = result.scalars().all()
        for edu in educations:
            stats["education"] += await self.index_education(edu.id)

        stats["total_chunks"] = sum(v for k, v in stats.items() if k != "total_chunks")

        logger.info(f"Full reindex completed: {stats}")
        return stats

    async def _delete_chunks(self, source_table: str, source_id: int):
        """Delete all chunks for a specific source"""
        await self.db.execute(
            delete(KnowledgeChunk).where(
                KnowledgeChunk.source_table == source_table,
                KnowledgeChunk.source_id == source_id
            )
        )
