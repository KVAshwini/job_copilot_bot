import re

from src.models import Job


TITLE_PATTERNS = [
    r"(?im)^\s*job title[:\-]\s*(.+)$",
    r"(?im)^\s*title[:\-]\s*(.+)$",
    r"(?im)^\s*role[:\-]\s*(.+)$",
]
COMPANY_PATTERNS = [
    r"(?im)^\s*company[:\-]\s*(.+)$",
    r"(?im)^\s*employer[:\-]\s*(.+)$",
]
LOCATION_PATTERNS = [
    r"(?im)^\s*location[:\-]\s*(.+)$",
    r"(?im)\b(remote|hybrid|onsite|on-site)\b.*",
]
SALARY_PATTERNS = [
    r"(?im)(\$[0-9][0-9,]*(?:\s*[-–]\s*\$?[0-9][0-9,]*)?(?:\s*(?:/year|per year|annually|hr|hour))?)",
]


def _first_match(patterns: list[str], text: str, default: str = "") -> str:
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return default


def source_from_url(url: str) -> str:
    lowered = url.lower()
    if "linkedin" in lowered:
        return "LinkedIn"
    if "indeed" in lowered:
        return "Indeed"
    if "greenhouse" in lowered:
        return "Greenhouse"
    if "lever" in lowered:
        return "Lever"
    return "Manual" if not url else "Company site"


def parse_job_description(description: str, url: str = "") -> Job:
    clean = description.strip()
    title = _first_match(TITLE_PATTERNS, clean, "Untitled role")
    company = _first_match(COMPANY_PATTERNS, clean, "Unknown company")
    location = _first_match(LOCATION_PATTERNS, clean, "")
    salary = _first_match(SALARY_PATTERNS, clean, "")
    return Job(
        title=title,
        company=company,
        location=location,
        salary=salary,
        source=source_from_url(url),
        url=url.strip(),
        description=clean,
    )


def extract_keywords(description: str) -> list[str]:
    known = [
        "Azure", "AWS", "GCP", "Kubernetes", "AKS", "Docker", "Terraform", "Jenkins",
        "GitHub Actions", "Azure DevOps", "CI/CD", "Linux", "Python", "Bash", "PowerShell",
        "Prometheus", "Grafana", "ELK", "Kafka", "SRE", "DevOps", "Incident Management",
        "Monitoring", "Networking", "Key Vault", "Helm", "ArgoCD", "SQL",
    ]
    lowered = description.lower()
    return sorted({keyword for keyword in known if keyword.lower() in lowered})
