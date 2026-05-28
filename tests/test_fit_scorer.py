from src.fit_scorer import score_job
from src.models import Job


def test_score_job_rewards_matching_devops_role() -> None:
    job = Job(
        title="DevOps Engineer",
        company="Example",
        location="Remote Canada",
        salary="$120,000",
        source="Manual",
        url="",
        description="Azure AKS Kubernetes Terraform CI/CD Linux Monitoring authorized to work remote",
    )
    preferences = {
        "skills": ["Azure", "AKS", "Kubernetes", "Terraform", "CI/CD", "Linux", "Monitoring"],
        "locations": ["remote", "canada"],
        "remote_preference": "remote_or_hybrid",
        "experience_level": "mid",
        "min_salary": 90000,
        "work_authorization": "authorized to work",
    }

    fit = score_job(job, preferences)

    assert fit.score >= 80
    assert "Kubernetes" in fit.details["skill_matches"]
    assert fit.details["remote_hybrid_match"]


def test_score_job_penalizes_poor_match() -> None:
    job = Job(
        title="Frontend Designer",
        company="Example",
        location="On-site Berlin",
        salary="$50,000",
        source="Manual",
        url="",
        description="Figma visual design sponsorship required",
    )

    fit = score_job(job, {"skills": ["Kubernetes", "Terraform"], "locations": ["remote"], "min_salary": 90000})

    assert fit.score < 40
