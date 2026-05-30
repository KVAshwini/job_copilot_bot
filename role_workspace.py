import streamlit as st

from src.role_profiles import get_role_profile, load_role_profiles, role_gap_analysis, role_job_search_terms
from src.utils import ROOT, read_text


MASTER_RESUME = ROOT / "data" / "master_resume.md"


def main() -> None:
    st.set_page_config(page_title="Aura Role Workspace", layout="wide")
    st.sidebar.title("Aura Role Workspace")
    st.sidebar.caption("Separate role planning UI. The main job dashboard stays in app.py.")

    profiles = load_role_profiles()
    labels = {profile["label"]: profile["key"] for profile in profiles}
    selected_label = st.sidebar.selectbox("Target role", list(labels))
    role_key = labels[selected_label]
    profile = get_role_profile(role_key)

    st.title(selected_label)
    st.write("Plan role-specific resume focus, keywords, screening answers, and job-search terms.")

    if not profile:
        st.error("Role profile not found.")
        return

    left, right = st.columns(2)
    with left:
        st.subheader("Target titles")
        for title in profile.get("target_titles", []):
            st.write(f"- {title}")

        st.subheader("Core skills")
        st.write(", ".join(profile.get("core_skills", [])))

        st.subheader("Resume focus")
        for item in profile.get("resume_focus", []):
            st.write(f"- {item}")

    with right:
        st.subheader("Screening questions")
        for question in profile.get("screening_questions", []):
            st.write(f"- {question}")

        st.subheader("Job search terms")
        st.code("\n".join(role_job_search_terms(role_key)))

    st.divider()
    st.subheader("Resume gap check")
    analysis = role_gap_analysis(read_text(MASTER_RESUME), role_key)
    st.write("Matched skills:")
    st.write(", ".join(analysis["matched_skills"]) or "No direct matches yet.")
    st.write("Missing or not explicit in master resume:")
    st.write(", ".join(analysis["missing_skills"]) or "None")
    st.warning("Only add missing skills to the resume if they are truthful and supported by real experience.")


if __name__ == "__main__":
    main()
