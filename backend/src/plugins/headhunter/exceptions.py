class HeadHunterError(Exception):
    """Base exception for the HeadHunter plugin."""

    pass


class HeadHunterDownloadPageError(HeadHunterError):
    """Exception for errors while downloading a page."""


class HHParsingTagNotFoundError(HeadHunterError):
    """HH parsing tag not found error."""


class HHVacancyInArchiveError(HeadHunterError):
    """HH vacancy in archive error."""

    pass


class HeadHunterSearchPageParsingError(HeadHunterError):
    """Exception for errors while parsing the search page."""

    pass


class HeadHunterVacancyPageParsingError(HeadHunterError):
    """Exception for errors while parsing the vacancy page."""

    pass
