from datetime import datetime
from pathlib import Path
from typing import Any

from db.database import connect, dumps, row_to_dict
from src.models import APPLICATION_STATUSES, Job


def add_job(job: Job, db_path: Path | None = None) -> int:
    with (connect(db_path) if db_path else connect()) as conn:
        cursor = conn.execute(
            """
            INSERT INTO jobs (title, company, location, salary, source, url, description, date_added, fit_score, fit_details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.title,
                job.company,
                job.location,
                job.salary,
                job.source,
                job.url,
                job.description,
                job.date_added,
                job.fit_score,
                job.fit_details,
            ),
        )
        job_id = int(cursor.lastrowid)
        conn.execute(
            "INSERT INTO applications (job_id, status, notes, date_updated) VALUES (?, ?, ?, ?)",
            (job_id, "not started", "", datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
        return job_id


def list_jobs(db_path: Path | None = None) -> list[dict[str, Any]]:
    with (connect(db_path) if db_path else connect()) as conn:
        rows = conn.execute("SELECT * FROM jobs ORDER BY date_added DESC").fetchall()
        return [row_to_dict(row) for row in rows]


def get_job(job_id: int, db_path: Path | None = None) -> dict[str, Any] | None:
    with (connect(db_path) if db_path else connect()) as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return row_to_dict(row) if row else None


def update_fit_score(job_id: int, score: int, details: dict, db_path: Path | None = None) -> None:
    with (connect(db_path) if db_path else connect()) as conn:
        conn.execute("UPDATE jobs SET fit_score = ?, fit_details = ? WHERE id = ?", (score, dumps(details), job_id))
        conn.commit()


def set_application_status(job_id: int, status: str, notes: str = "", db_path: Path | None = None) -> None:
    if status not in APPLICATION_STATUSES:
        raise ValueError(f"Invalid status: {status}")
    with (connect(db_path) if db_path else connect()) as conn:
        conn.execute(
            "INSERT INTO applications (job_id, status, notes, date_updated) VALUES (?, ?, ?, ?)",
            (job_id, status, notes, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()


def latest_applications(db_path: Path | None = None) -> list[dict[str, Any]]:
    with (connect(db_path) if db_path else connect()) as conn:
        rows = conn.execute(
            """
            SELECT j.id AS job_id, j.title, j.company, j.location, j.fit_score, a.status, a.notes, a.date_updated
            FROM jobs j
            JOIN applications a ON a.id = (
                SELECT id FROM applications WHERE job_id = j.id ORDER BY date_updated DESC, id DESC LIMIT 1
            )
            ORDER BY a.date_updated DESC
            """
        ).fetchall()
        return [row_to_dict(row) for row in rows]


def save_resume(job_id: int, summary: str, skills: list[str], bullets: list[str], missing: list[str], db_path: Path | None = None) -> None:
    with (connect(db_path) if db_path else connect()) as conn:
        conn.execute(
            "INSERT INTO resumes (job_id, summary, skills, bullets, missing_keywords, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (job_id, summary, dumps(skills), dumps(bullets), dumps(missing), datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()


def save_cover_letter(job_id: int, content: str, db_path: Path | None = None) -> None:
    with (connect(db_path) if db_path else connect()) as conn:
        conn.execute(
            "INSERT INTO cover_letters (job_id, content, created_at) VALUES (?, ?, ?)",
            (job_id, content, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()


def save_generated_answer(answer_type: str, question: str, answer: str, job_id: int | None = None, db_path: Path | None = None) -> None:
    with (connect(db_path) if db_path else connect()) as conn:
        conn.execute(
            "INSERT INTO generated_answers (job_id, answer_type, question, answer, created_at) VALUES (?, ?, ?, ?, ?)",
            (job_id, answer_type, question, answer, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()
