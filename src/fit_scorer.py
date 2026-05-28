import re

from src.jd_parser import extract_keywords
from src.models import FitScore, Job
from src.utils import keyword_hits, normalize, read_json


DEFAULT_SKILLS = [
    "Azure", "AKS", "Kubernetes", "Docker", "Terraform", "CI/CD", "Azure DevOps",
    "GitHub Actions", "Jenkins", "Linux", "Monitoring", "Prometheus", "Grafana",
    "Kafka", "Python", "Bash", "PowerShell", "Incident Management", "SRE",
]


def _score_ratio(matches: int, total: int, weight: int) -> int:
    if total == 0:
        return 0
    return round((matches / total) * weight)


def _experience_level(description: str) -> str:
    lowered = description.lower()
    if any(term in lowered for term in ["senior", "lead", "principal", "7+ years", "8+ years", "10+ years"]):
        return "senior"
    if any(term in lowered for term in ["junior", "entry level", "0-2 years", "1+ years"]):
        return "junior"
    return "mid"


def _salary_number(value: str) -> int | None:
    match = re.search(r"([0-9][0-9,]{2,})", value)
    return int(match.group(1).replace(",", "")) if match else None


def score_job(job: Job, preferences: dict | None = None) -> FitScore:
    preferences = preferences or {}
    preferred_skills = preferences.get("skills", DEFAULT_SKILLS)
    preferred_locations = [normalize(item) for item in preferences.get("locations", [])]
    remote_preference = preferences.get("remote_preference", "remote_or_hybrid")
    min_salary = preferences.get("min_salary")
    authorization = normalize(preferences.get("work_authorization", ""))

    description = job.description + " " + job.title + " " + job.location
    jd_keywords = extract_keywords(description)
    skill_matches = keyword_hits(description, preferred_skills)
    devops_matches = keyword_hits(description, ["DevOps", "SRE", "CI/CD", "Kubernetes", "Terraform", "Azure", "Monitoring"])

    location_text = normalize(job.location + " " + job.description)
    location_match = bool(preferred_locations and any(loc in location_text for loc in preferred_locations))
    remote_match = (
        remote_preference == "any"
        or ("remote" in location_text and remote_preference in {"remote", "remote_or_hybrid"})
        or ("hybrid" in location_text and remote_preference in {"hybrid", "remote_or_hybrid"})
    )
    level = _experience_level(job.description)
    preferred_level = preferences.get("experience_level", "mid")
    experience_match = level == preferred_level or preferred_level == "mid" and level in {"mid", "senior"}
    salary_value = _salary_number(job.salary)
    salary_match = min_salary is None or salary_value is None or salary_value >= int(min_salary)
    auth_match = not authorization or authorization in normalize(job.description) or "sponsorship" not in normalize(job.description)

    score = 0
    score += _score_ratio(len(skill_matches), max(len(preferred_skills), 1), 35)
    score += _score_ratio(len(devops_matches), 7, 20)
    score += 10 if location_match else 4 if not preferred_locations else 0
    score += 10 if remote_match else 0
    score += 10 if experience_match else 3
    score += 8 if salary_match else 0
    score += 7 if auth_match else 0
    score = min(100, score)

    return FitScore(
        score=score,
        details={
            "skill_matches": skill_matches,
            "job_keywords": jd_keywords,
            "devops_cloud_matches": devops_matches,
            "location_match": location_match,
            "remote_hybrid_match": remote_match,
            "experience_level": level,
            "experience_match": experience_match,
            "salary_match": salary_match,
            "work_authorization_fit": auth_match,
        },
    )


def load_preferences(path) -> dict:
    return read_json(path, {})
