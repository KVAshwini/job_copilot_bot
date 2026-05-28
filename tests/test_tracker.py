from pathlib import Path

import pytest

from db.database import init_db
from src.models import Job
from src.tracker import add_job, latest_applications, list_jobs, set_application_status, update_fit_score


def test_tracker_database_operations(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    job = Job(
        title="DevOps Engineer",
        company="Example",
        location="Remote",
        salary="$100,000",
        source="Manual",
        url="https://example.com",
        description="Kubernetes Terraform CI/CD",
    )

    job_id = add_job(job, db_path=db_path)
    update_fit_score(job_id, 88, {"skill_matches": ["Kubernetes"]}, db_path=db_path)
    set_application_status(job_id, "prepared", "Resume tailored", db_path=db_path)

    jobs = list_jobs(db_path=db_path)
    applications = latest_applications(db_path=db_path)

    assert jobs[0]["fit_score"] == 88
    assert applications[0]["status"] == "prepared"


def test_invalid_status_rejected(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)

    with pytest.raises(ValueError):
        set_application_status(1, "auto submitted", db_path=db_path)
