from pathlib import Path

from db.database import init_db
from src.apply_assistant import build_application_packet, readiness_score
from src.models import Job
from src.tracker import add_job, latest_application_packets, save_application_packet


def test_application_packet_uses_common_answers() -> None:
    job = Job(
        id=7,
        title="Platform Engineer",
        company="Example",
        location="Remote",
        salary="",
        source="Manual",
        url="https://example.com",
        description="Please include email, work authorization, sponsorship, salary, and resume.",
    )
    packet = build_application_packet(
        job,
        {
            "work_authorization": "Authorized to work in Canada.",
            "sponsorship": "No sponsorship required.",
            "salary_expectation": "Flexible.",
        },
        {"email": "candidate@example.com"},
    )

    assert packet["manual_submit_required"] is True
    assert packet["answers"]["email"] == "candidate@example.com"
    assert packet["answers"]["work_authorization"] == "Authorized to work in Canada."
    assert "resume" not in packet["answers"]


def test_readiness_score_tracks_missing_answers() -> None:
    score, missing = readiness_score({"email": "a@example.com", "phone": ""})

    assert score == 50
    assert missing == ["phone"]


def test_application_packet_persists_with_existing_jobs(tmp_path: Path) -> None:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    job_id = add_job(
        Job(
            title="QA Engineer",
            company="Example",
            location="Remote",
            salary="",
            source="Manual",
            url="https://example.com",
            description="Email and work authorization required.",
        ),
        db_path=db_path,
    )
    packet = {"readiness_score": 100, "missing_fields": [], "answers": {"email": "a@example.com"}, "manual_submit_required": True}

    packet_id = save_application_packet(job_id, packet, db_path=db_path)
    packets = latest_application_packets(db_path=db_path)

    assert packet_id == 1
    assert packets[0]["job_id"] == job_id
    assert packets[0]["readiness_score"] == 100
