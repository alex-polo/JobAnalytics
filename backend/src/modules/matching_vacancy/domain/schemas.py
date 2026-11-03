from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class ResumeMatchInput(BaseModel):
    """Vacancy match input."""

    resume_text: str
    vacancy_text: str


class MatchLevel(Enum):
    """Level of match."""

    perfect = "perfect"  # 90-100%
    strong = "strong"  # 70-89%
    moderate = "moderate"  # 50-69%
    weak = "weak"  # 30-49%
    mismatch = "mismatch"  # 0-29%


class LocationItems(Enum):
    """Location of match."""

    remote = "remote"
    office = "office"
    gibrid = "gibrid"


class AIPluginResumeMatchOutput(BaseModel):
    """Resume match output."""

    match_score: int = Field(ge=0, le=100, description="Процент соответствия 0-100")
    match_level: MatchLevel = Field(
        description=(
            "Категория соответствия. Должна строго соответствовать match_score:\n"
            "- perfect: если match_score от 90 до 100\n"
            "- strong: если match_score от 70 до 89\n"
            "- moderate: если match_score от 50 до 69\n"
            "- weak: если match_score от 30 до 49\n"
            "- mismatch: если match_score от 0 до 29"
        )
    )

    # Details
    matching_skills: list[str] = Field(description="Совпадающие навыки")
    missing_skills: list[str] = Field(description="Чего не хватает кандидату")
    extra_skills: list[str] = Field(description="Лишние навыки кандидата")

    # Key points
    experience_match: bool = Field(description="Опыт соответствует уровню вакансии")
    level_match: bool = Field(description="Уровень кандидата = уровню вакансии")
    location_match: bool = Field(
        description="Можно ли по этой вакансии работать удаленно"
    )
    salary_match: bool | None = Field(default=None, description="Зарплата в рамках")
    location: LocationItems = Field(
        description="Место работы, удаленная, офис или гибрид"
    )

    # Recomendations
    summary: str = Field(description="Краткое резюме оценки в 3-4 предложениях")
    strengths: list[str] = Field(
        description="Сильные стороны кандидата для этой вакансии"
    )
    gaps: list[str] = Field(description="Слабые стороны / пробелы")
    recommendation: str = Field(description="Пригласить/отклонить/рассмотреть")


class ResumeMatchListItem(BaseModel):
    """Resume match list item."""

    id: int
    vacancy_title: str
    resume_title: str
    match_score: int
    match_level: MatchLevel
    keyword: str
    salary: str
    location: LocationItems
    location_match: bool
    url: str
    created_at: datetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class ResumeMatchDetails(BaseModel):
    """Resume match output."""

    id: int
    resume_id: int
    vacancy_id: int

    url: str
    keyword: str

    match_score: int = Field(ge=0, le=100)
    match_level: MatchLevel

    matching_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]

    experience_match: bool
    level_match: bool
    location_match: bool
    salary_match: bool | None = None
    location: LocationItems

    summary: str
    strengths: list[str]
    gaps: list[str]
    recommendation: str

    prompt_name: str | None = None
    prompt_version: str | None = None
    prompt_locale: str | None = None
    model_name: str | None = None
    finish_reason: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
