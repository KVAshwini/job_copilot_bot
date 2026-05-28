from src.jd_parser import extract_keywords, parse_job_description, source_from_url


def test_parse_job_description_extracts_basic_fields() -> None:
    jd = """
    Job Title: DevOps Engineer
    Company: Aura Systems
    Location: Remote Canada
    Salary: $110,000 - $130,000

    We need Azure, Kubernetes, Terraform, Linux, and CI/CD experience.
    """

    job = parse_job_description(jd, "https://company.example/jobs/123")

    assert job.title == "DevOps Engineer"
    assert job.company == "Aura Systems"
    assert job.location == "Remote Canada"
    assert "$110,000" in job.salary
    assert job.source == "Company site"


def test_source_from_url_identifies_known_boards() -> None:
    assert source_from_url("https://linkedin.com/jobs/view/1") == "LinkedIn"
    assert source_from_url("https://indeed.com/viewjob?jk=1") == "Indeed"


def test_extract_keywords() -> None:
    keywords = extract_keywords("Azure AKS Kubernetes Terraform Grafana")
    assert {"Azure", "AKS", "Kubernetes", "Terraform", "Grafana"} <= set(keywords)
