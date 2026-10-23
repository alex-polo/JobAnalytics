from enum import Enum

from pydantic import BaseModel, Field


class MatchLevel(Enum):
    """Уровень совпадения."""

    perfect = "perfect"  # 90-100%
    strong = "strong"  # 70-89%
    moderate = "moderate"  # 50-69%
    weak = "weak"  # 30-49%
    mismatch = "mismatch"  # 0-29%


class ResumeAnalysis(BaseModel):
    """Результат анализа резюме."""

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
    location_match: bool = Field(description="Локация/удалёнка подходят")
    salary_match: bool | None = Field(default=None, description="Зарплата в рамках")

    # Recomendations

    summary: str = Field(description="Краткое резюме оценки в 3-4 предложениях")
    strengths: list[str] = Field(
        description="Сильные стороны кандидата для этой вакансии"
    )
    gaps: list[str] = Field(description="Слабые стороны / пробелы")
    recommendation: str = Field(description="Пригласить/отклонить/рассмотреть")
