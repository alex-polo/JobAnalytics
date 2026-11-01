from dataclasses import dataclass


@dataclass(frozen=True)
class QueueMatchingClaimedItem:
    """Claimed item."""

    id: int
    resume_id: int
    raw_vacancy_id: int
    vacancy_keyword: str
    attempts: int
