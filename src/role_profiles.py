from pathlib import Path
from typing import Any

from src.utils import ROOT, keyword_hits, read_json


ROLE_PROFILE_PATH = ROOT / "data" / "role_profiles.json"


def load_role_profiles(path: Path = ROLE_PROFILE_PATH) -> list[dict[str, Any]]:
    return read_json(path, [])


def get_role_profile(role_key: str) -> dict[str, Any] | None:
    for profile in load_role_profiles():
        if profile["key"] == role_key:
            return profile
    return None


def role_gap_analysis(master_resume: str, role_key: str) -> dict[str, list[str]]:
    profile = get_role_profile(role_key)
    if not profile:
        return {"matched_skills": [], "missing_skills": [], "resume_focus": []}
    core_skills = profile.get("core_skills", [])
    matched = keyword_hits(master_resume, core_skills)
    missing = [skill for skill in core_skills if skill not in matched]
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_focus": profile.get("resume_focus", []),
    }


def role_job_search_terms(role_key: str) -> list[str]:
    profile = get_role_profile(role_key)
    if not profile:
        return []
    return profile.get("target_titles", []) + profile.get("core_skills", [])
