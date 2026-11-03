import html
import json
import logging
from typing import Any

from bs4 import BeautifulSoup, Tag

from src.plugins.sources.headhunter.exceptions import (
    HeadHunterVacancyPageParsingError,
    HHParsingAdvertisingRedirectError,
    HHParsingTagNotFoundError,
    HHVacancyInArchiveError,
)

from .schemas import VacancyParsingEntityV2

log = logging.getLogger(__name__)

EXPERIENCE_MAP: dict[str, str] = {
    "noExperience": "Нет опыта",
    "between1And3": "1–3 года",  # noqa: RUF001
    "between3And6": "3–6 лет",  # noqa: RUF001
    "moreThan6": "Более 6 лет",
}


def _dig(obj: Any, *path: str, default: Any = None) -> Any:  # noqa: ANN401
    """Safely traverse nested dicts by keys, return def if missing."""
    cur = obj
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


def _unescape_text(value: Any) -> Any:  # noqa: ANN401
    """Unescape HTML entities in a single text value.

    Apply only to fields that contain HTML entities in the original
    hh.ru JSON (e.g. vacancy description, names, dictionary texts).
    Do NOT apply to the whole JSON string: it breaks escaping inside
    nested JSON strings (applicationLdJSON, siteCounterGroups[].content)
    """
    if isinstance(value, str):
        return html.unescape(value)
    return value


def _build_dictionary(data: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Build id->text lookup maps for vacancy reference dictionaries."""
    src = data.get("vacancyFieldsDictionary") or {}
    return {
        key: {
            item["id"]: _unescape_text(item["text"])
            for item in src.get(key, [])
            if "id" in item and "text" in item
        }
        for key in (
            "employmentForm",
            "workFormats",
            "workScheduleByDays",
            "workingHours",
            "civilLawContract",
        )
    }


def _translate_many(dictionary: dict[str, str], ids: list[str] | None) -> list[str]:
    """Translate a list of ids into texts, keeping unknown ids as-is."""
    if not ids:
        return []
    return [dictionary.get(i, i) for i in ids]


def _format_salary(compensation: dict[str, Any] | None) -> str:
    """Format salary range as a human-readable string."""
    if not compensation or compensation.get("noCompensation"):
        return "Уровень дохода не указан"

    frm = compensation.get("from")
    to = compensation.get("to")
    currency = compensation.get("currencyCode", "")

    if frm and to:
        return f"{frm} – {to} {currency}".strip()  # noqa: RUF001
    if frm:
        return f"от {frm} {currency}".strip()
    if to:
        return f"до {to} {currency}".strip()
    return "Уровень дохода не указан"


def _get_experience(data: dict[str, Any], vacancy: dict[str, Any]) -> str | None:
    """Resolve the human-readable work experience requirement."""
    translated = _dig(data, "vacancyView", "translations", "workExperience")
    if translated:
        return _unescape_text(translated)

    raw = vacancy.get("workExperience")
    if not raw:
        return None
    return EXPERIENCE_MAP.get(raw, raw)


def _get_civil_contract(
    vacancy: dict[str, Any],
    dicts: dict[str, dict[str, str]],
) -> str | None:
    """Build a human-readable employment contract description."""
    if vacancy.get("acceptLaborContract"):
        return "Трудовой договор"

    civil = _translate_many(dicts["civilLawContract"], vacancy.get("civilLawContracts"))
    if not civil:
        return None
    return "Договор ГПХ " + ", ".join(civil)


def _build_description_header(
    title: str | None,
    salary: str,
    experience: str | None,
    employment: str | None,
    civil_contract: str | None,
    schedule: str | None,
    working_hours: str | None,
    work_formats: str | None,
) -> str:
    """Build a short vacancy header from parsed attributes."""
    lines: list[str] = []

    if title:
        lines.append(title)
    if salary:
        lines.append(salary)
    if experience:
        lines.append(f"Опыт работы: {experience}")
    if employment:
        lines.append(f"Тип занятости: {employment}")
    if civil_contract:
        lines.append(f"Оформление: {civil_contract}")
    if schedule:
        lines.append(f"График: {schedule}")
    if working_hours:
        lines.append(f"Рабочие часы: {working_hours.lower()}")
    if work_formats:
        lines.append(f"Формат работы: {work_formats.lower()}")

    return "\n".join(lines)


def _is_archived(
    vacancy_json: dict[str, Any],
    vacancy: dict[str, Any],
) -> tuple[bool, dict[str, Any]]:
    """Detect whether the vacancy is archived.

    Returns a tuple (is_archived, signals) where signals is a dict
    of raw archive indicators used for diagnostics.
    """
    signals: dict[str, Any] = {
        "analyticsParams.archived": _dig(vacancy_json, "analyticsParams", "archived"),
        "status.archived": _dig(vacancy, "status", "archived"),
        "status.hiddenInArchive": _dig(vacancy, "status", "hiddenInArchive"),
        "status.disabled": _dig(vacancy, "status", "disabled"),
        "systemInfo": _dig(
            vacancy_json,
            "vacancyView",
            "vacancyFull",
            "systemInfo",
            default=None,
        ),
    }

    # analyticsParams.archived comes as the string "true"/"false".
    archived_flag = str(signals["analyticsParams.archived"]).lower() == "true"
    is_archived = (
        archived_flag
        or signals["status.archived"] is True
        or signals["status.hiddenInArchive"] is True
        or signals["status.disabled"] is True
        or signals["systemInfo"] is not None
    )
    return is_archived, signals


def parsing_vacancy_page(
    html_content: str,
    url: str,
) -> VacancyParsingEntityV2:
    """Parse the HTML content of an hh.ru vacancy page."""
    try:
        soup = BeautifulSoup(html_content, "lxml")
        tpl_tag: Tag | None = soup.find("template", id="HH-Lux-InitialState")

        if not tpl_tag:
            raise HHParsingTagNotFoundError(
                'Tag "<template id="HH-Lux-InitialState">" not found.'
            )

        raw = tpl_tag.string or tpl_tag.get_text()
        if not raw or not raw.strip():
            raise HHParsingTagNotFoundError(
                'Tag "<template id="HH-Lux-InitialState">" is empty.'
            )

        # Do NOT apply html.unescape to the whole string: the JSON in
        # <template> is already valid. Global unescape breaks escaping
        # inside nested JSON strings (applicationLdJSON,
        # siteCounterGroups[].content), inserting real `"` characters
        # and causing json.loads to fail with "Expecting ',' delimiter".
        # HTML entities are decoded selectively below, per text field.
        vacancy_json = json.loads(raw)

        vacancy = (
            _dig(
                vacancy_json,
                "vacancyView",
                "vacancyFull",
                "vacancy",
                default={},
            )
            or {}
        )

        # 1) Archived vacancy: short-circuit before building the header.
        is_archived, archive_signals = _is_archived(vacancy_json, vacancy)
        if is_archived:
            triggered = {k: v for k, v in archive_signals.items() if v}
            raise HHVacancyInArchiveError(
                f"Vacancy {url} is archived (signals: {triggered})."
            )

        # 2) Not archived but required fields are missing: this is
        # broken data, not an archived vacancy.
        # Name and description contain HTML entities in hh.ru JSON,
        # so decode them selectively here.
        title = _unescape_text(vacancy.get("name"))
        body = _unescape_text(vacancy.get("description"))
        if not title or not body:
            missing = [k for k, v in (("name", title), ("description", body)) if not v]
            log.error(f"Vacancy {vacancy_json}: {vacancy_json}")

            raise HeadHunterVacancyPageParsingError(
                f"Vacancy {url}: missing required fields {missing} "
                f"in HH-Lux-InitialState."
            )

        dicts: dict[str, dict[str, str]] = _build_dictionary(vacancy_json)

        salary = _format_salary(vacancy.get("compensation"))
        experience = _get_experience(vacancy_json, vacancy)

        employment_list = _translate_many(
            dicts["employmentForm"],
            [vacancy["employmentForm"]] if vacancy.get("employmentForm") else [],
        )
        employment: str | None = ", ".join(employment_list) if employment_list else None

        civil_contract: str | None = _get_civil_contract(vacancy, dicts)

        schedule_list: list[str] = _translate_many(
            dicts["workScheduleByDays"],
            vacancy.get("workScheduleByDays"),
        )
        schedule: str | None = ", ".join(schedule_list) if schedule_list else None

        working_hours_list: list[str] = _translate_many(
            dicts["workingHours"], vacancy.get("workingHours")
        )
        working_hours: str | None = (
            ", ".join(working_hours_list) if working_hours_list else None
        )

        work_formats_list: list[str] = _translate_many(
            dicts["workFormats"], vacancy.get("workFormats")
        )
        work_formats: str | None = (
            ", ".join(work_formats_list) if work_formats_list else None
        )

        description: str = _build_description_header(
            title=title,
            salary=salary,
            experience=experience,
            employment=employment,
            civil_contract=civil_contract,
            schedule=schedule,
            working_hours=working_hours,
            work_formats=work_formats,
        )

        company_name = _unescape_text(_dig(vacancy, "company", "name"))

        return VacancyParsingEntityV2(
            title=title,
            salary=salary,
            experience=experience,
            employment=employment,
            civil_contract=civil_contract,
            schedule=schedule,
            working_hours=working_hours,
            work_formats=work_formats,
            url=url,
            description=description,
            body=body,
            company_name=company_name,
            html_content=html_content,
        )
    except (
        HHParsingTagNotFoundError,
        HHParsingAdvertisingRedirectError,
        HHVacancyInArchiveError,
    ):
        # Explicit business exceptions are re-raised as-is.
        raise
    except json.JSONDecodeError as exc:
        raise HeadHunterVacancyPageParsingError(
            f"Invalid JSON in HH-Lux-InitialState for {url}: {exc}"
        ) from exc
    except HeadHunterVacancyPageParsingError:
        # Already our error, do not wrap again.
        raise
    except Exception as exc:
        raise HeadHunterVacancyPageParsingError(
            f"Error while parsing vacancy page {url}: {exc}"
        ) from exc
