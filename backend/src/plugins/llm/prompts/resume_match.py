from typing import Final

PROMPT_VERSION: Final[str] = "1"
PROMPT_LOCALE: Final[str] = "ru"

SYSTEM_PROMPT: Final[str] = (
    "Ты — HR-аналитик. Извлекай структурированную информацию из вакансий."
    "ПРАВИЛА:"
    "- Анализируй только то, что явно указано в резюме"
    "- Не додумывай требования, которых нет в тексте"  # noqa: RUF001
    "- Отвечай строго в формате JSON"
)

HUMAN_PROMPT: Final[str] = (
    "Проанализируй на соответствие следующие данные:\n\n"
    "ТЕКСТ РЕЗЮМЕ:\n"  # noqa: RUF001
    "{resume_text}\n\n"
    "ДАННЫЕ ВАКАНСИИ:\n"
    "{vacancy_text}"
)
