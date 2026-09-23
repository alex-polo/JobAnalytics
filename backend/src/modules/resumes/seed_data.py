import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from PyPDF2 import PdfReader
from sqlalchemy import select

from src.modules.resumes.infrastructure.models import KeywordsResumeORM, ResumeORM
from src.modules.sources.infrastructure.models import SourceORM

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

log = logging.getLogger(__name__)


INITIAL_RESUMES: Final[list[dict[str, Any]]] = [
    {
        "name": "python_developer",
        "filename": "python_developer.pdf",
        "keywords": [
            "python",
            "FastAPI",
            "Django",
            "SQLAlchemy",
        ],
        "source_codes": [
            "hh",
        ],
        "is_active": True,
    },
]


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from PDF file."""
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    text_parts = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_parts.append(text)

    return "\n".join(text_parts).strip()


async def seed_resumes(async_sessionmaker: async_sessionmaker[AsyncSession]) -> None:
    """Populate sources table with initial data."""
    async with async_sessionmaker() as session:
        result_sources = await session.execute(select(SourceORM))
        sources_by_code = {
            source.code: source for source in result_sources.scalars().all()
        }

        for resume_data in INITIAL_RESUMES:
            result_resume = await session.execute(
                select(ResumeORM).where(ResumeORM.name == resume_data["name"])
            )
            resume_existing: ResumeORM | None = result_resume.scalar_one_or_none()

            if not resume_existing:
                pdf_filename = Path(f"data/resumes/{resume_data['filename']}")

                try:
                    text_content = extract_text_from_pdf(pdf_filename)
                except FileNotFoundError as e:
                    log.error(f"Skipping resume {resume_data['name']}: {e}")
                    continue

                # Creating resume
                resume = ResumeORM(
                    name=resume_data["name"],
                    text=text_content,
                )

                # Adding keywords
                resume.keywords = [
                    KeywordsResumeORM(keyword=kw) for kw in resume_data["keywords"]
                ]

                # Adding sources
                sources = [
                    sources_by_code[code]
                    for code in resume_data["source_codes"]
                    if code in sources_by_code
                ]
                resume.sources = sources

                session.add(resume)
                log.info(
                    f"Added resume: {resume_data['name']} (from {resume_data['filename']})"  # noqa: E501
                )
            else:
                log.info(f"Resume already exists: {resume_data['name']}")

        await session.commit()
        log.info("Resumes seeding completed successfully.")
