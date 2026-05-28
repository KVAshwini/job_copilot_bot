from dataclasses import dataclass, field
from datetime import datetime


APPLICATION_STATUSES = [
    "not started",
    "prepared",
    "applied",
    "recruiter contacted",
    "interview scheduled",
    "rejected",
    "offer",
    "follow-up needed",
]


@dataclass(frozen=True)
class Job:
    title: str
    company: str
    location: str
    salary: str
    source: str
    url: str
    description: str
    date_added: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    id: int | None = None
    fit_score: int | None = None
    fit_details: str | None = None


@dataclass(frozen=True)
class FitScore:
    score: int
    details: dict[str, object]


@dataclass(frozen=True)
class TailoredResume:
    summary: str
    skills: list[str]
    bullets: list[str]
    missing_keywords: list[str]
