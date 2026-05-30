from src.role_profiles import get_role_profile, role_gap_analysis, role_job_search_terms


def test_role_profile_loads_qa() -> None:
    profile = get_role_profile("qa")

    assert profile is not None
    assert "QA Engineer" in profile["label"]
    assert "API Testing" in profile["core_skills"]


def test_role_gap_analysis_identifies_missing_skills() -> None:
    analysis = role_gap_analysis("Azure Kubernetes Terraform", "qa")

    assert "API Testing" in analysis["missing_skills"]
    assert analysis["resume_focus"]


def test_role_job_search_terms_include_titles_and_skills() -> None:
    terms = role_job_search_terms("developer")

    assert "Software Developer" in terms
    assert "APIs" in terms
