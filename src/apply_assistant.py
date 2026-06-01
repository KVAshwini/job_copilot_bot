from src.field_detector import detect_likely_fields
from src.models import Job


DEFAULT_FIELDS = [
    "name",
    "email",
    "phone",
    "location",
    "work_authorization",
    "sponsorship",
    "salary_expectation",
    "notice_period",
]


def build_answer_library(common_answers: dict, profile_overrides: dict | None = None) -> dict[str, str]:
    profile = profile_overrides or {}
    return {
        "name": profile.get("name", ""),
        "email": profile.get("email", ""),
        "phone": profile.get("phone", ""),
        "location": profile.get("location", ""),
        "work_authorization": common_answers.get("work_authorization", ""),
        "sponsorship": common_answers.get("sponsorship", ""),
        "salary_expectation": common_answers.get("salary_expectation", ""),
        "notice_period": common_answers.get("notice_period", ""),
        "relocation": common_answers.get("relocation", ""),
        "remote_hybrid_preference": common_answers.get("remote_hybrid_preference", ""),
        "years_of_experience": common_answers.get("years_of_experience", ""),
        "why_this_company": common_answers.get("why_this_company", ""),
        "why_this_role": common_answers.get("why_this_role", ""),
    }


def build_answers(answer_library: dict[str, str], job_description: str) -> dict[str, str]:
    fields = detect_likely_fields(job_description)
    if not fields:
        fields = DEFAULT_FIELDS
    return {field: answer_library.get(field, "") for field in fields if field in answer_library}


def readiness_score(answers: dict[str, str]) -> tuple[int, list[str]]:
    if not answers:
        return 0, []
    missing = [field for field, value in answers.items() if not value.strip()]
    score = round(((len(answers) - len(missing)) / len(answers)) * 100)
    return score, missing


def build_application_packet(job: Job, common_answers: dict, profile_overrides: dict | None = None) -> dict:
    answer_library = build_answer_library(common_answers, profile_overrides)
    answers = build_answers(answer_library, job.description)
    score, missing = readiness_score(answers)
    return {
        "job_id": job.id,
        "readiness_score": score,
        "missing_fields": missing,
        "answers": answers,
        "manual_submit_required": True,
    }
