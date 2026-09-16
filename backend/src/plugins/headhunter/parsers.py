import logging

from bs4 import BeautifulSoup, Tag

from .exceptions import HHParsingTagNotFoundError, HHVacancyInArchiveError
from .schemas import VacancyParsingEntity, VacancySearchParsingEntity

log = logging.getLogger(__name__)


def get_inner_tag(
    html_tag: Tag,
    tag_name: str,
    class_name: str | None = None,
    data_qa: str | None = None,
) -> Tag:
    """Get inner HTML tag."""
    if class_name and data_qa:
        inner_tag: Tag | None = html_tag.find(
            tag_name,
            {"class": class_name, "data-qa": data_qa},
        )
    elif class_name:
        inner_tag: Tag | None = html_tag.find(
            tag_name,
            class_=class_name,
        )
    else:
        inner_tag: Tag | None = html_tag.find(tag_name)

    if not inner_tag:
        details = f"Tag: {tag_name}, class: {class_name}, data-qa: {data_qa}"
        raise HHParsingTagNotFoundError(details)

    return inner_tag


def parsing_search_page(html_content: str) -> list:
    """Parse page vacancies."""
    log.info("Parsing search page...")
    soup = BeautifulSoup(html_content, "lxml")
    results_section: Tag | None = soup.find(
        "section",
        {"data-qa": "vacancy-serp__results"},
    )

    if not results_section:
        raise HHParsingTagNotFoundError(
            'Tag <section data-qa="vacancy-serp__results"> not found.'
        )

    vacancies_items = results_section.find_all("article")
    vacancies: list[VacancySearchParsingEntity] = []

    for vacancy_item in vacancies_items:
        tag_a: Tag | None = vacancy_item.find("a", {"data-qa": "serp-item__title"})
        tag_a = get_inner_tag(
            vacancy_item,
            "a",
            data_qa="serp-item__title",
        )

        vacancy_title = tag_a.text
        vacancy_link = str(tag_a["href"])

        vacancies.append(
            VacancySearchParsingEntity(title=vacancy_title, url=vacancy_link)
        )
    log.info("Vacancies search page parsed successfully.")

    return vacancies


def parse_vacancy_page(html_content: str, url: str) -> VacancyParsingEntity:
    """Parse vacancies."""
    log.info("Parsing vacancy page...")

    soup = BeautifulSoup(html_content, "lxml")

    vacancy_section: Tag | None = soup.find("div", class_="bloko-columns-row")

    if not vacancy_section:
        raise HHParsingTagNotFoundError(
            'Tag <div class="bloko-columns-row"> not found.'
        )

    is_archive: bool = (
        get_inner_tag(vacancy_section, "h2", data_qa="bloko-header-2").text
        == "Вакансия в архиве"
    )
    if is_archive:
        raise HHVacancyInArchiveError(f"Vacancy {url} is in archive.")

    title = get_inner_tag(
        get_inner_tag(vacancy_section, "div", class_name="vacancy-title"),
        "h1",
    ).text
    description = get_inner_tag(
        vacancy_section,
        "div",
        class_name="magritte-flex-container___CVFEY_8-6-7",
    ).text
    vacancy_body = get_inner_tag(
        vacancy_section,
        "div",
        class_name="g-user-content",
        data_qa="vacancy-description",
    ).text

    log.info("Vacancy page parsed successfully.")

    return VacancyParsingEntity(
        title=title,
        url=url,
        description=description,
        body=vacancy_body,
    )
