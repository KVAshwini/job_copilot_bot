from src.jd_parser import parse_job_description
from src.models import Job


def build_job_from_input(
    description: str,
    url: str = "",
    title: str = "",
    company: str = "",
    location: str = "",
    salary: str = "",
) -> Job:
    parsed = parse_job_description(description, url)
    return Job(
        title=title.strip() or parsed.title,
        company=company.strip() or parsed.company,
        location=location.strip() or parsed.location,
        salary=salary.strip() or parsed.salary,
        source=parsed.source,
        url=url.strip(),
        description=description.strip(),
    )
