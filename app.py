from pathlib import Path

import streamlit as st

from db.database import DB_PATH, init_db, loads
from src.browser_helper import clipboard_instruction, open_application_url
from src.fit_scorer import load_preferences, score_job
from src.job_importer import build_job_from_input
from src.message_generator import cover_letter, email_application_message, followup_message, linkedin_message
from src.models import APPLICATION_STATUSES, Job
from src.resume_tailor import tailor_resume
from src.tracker import (
    add_job,
    latest_applications,
    list_jobs,
    save_cover_letter,
    save_generated_answer,
    save_resume,
    set_application_status,
    update_fit_score,
)
from src.utils import ROOT, read_json, read_text


st.set_page_config(page_title="Aura Job Copilot", layout="wide")
init_db()

MASTER_RESUME = ROOT / "data" / "master_resume.md"
PREFERENCES = ROOT / "data" / "job_preferences.json"
COMMON_ANSWERS = ROOT / "data" / "common_application_answers.json"


def job_options() -> dict[str, int]:
    jobs = list_jobs()
    return {f"#{job['id']} - {job['title']} at {job['company']}": job["id"] for job in jobs}


def selected_job() -> dict | None:
    options = job_options()
    if not options:
        st.info("Add a job first.")
        return None
    label = st.selectbox("Job", list(options))
    return next(job for job in list_jobs() if job["id"] == options[label])


def to_job(row: dict) -> Job:
    return Job(
        id=row["id"],
        title=row["title"],
        company=row["company"],
        location=row.get("location") or "",
        salary=row.get("salary") or "",
        source=row.get("source") or "",
        url=row.get("url") or "",
        description=row.get("description") or "",
        date_added=row.get("date_added") or "",
        fit_score=row.get("fit_score"),
        fit_details=row.get("fit_details"),
    )


st.sidebar.title("Aura Job Copilot")
page = st.sidebar.radio(
    "Pages",
    [
        "Add Job",
        "Match Score",
        "Tailor Resume",
        "Generate Messages",
        "Application Tracker",
        "Follow-ups",
        "Settings",
    ],
)
st.sidebar.caption("Local-first. Human-in-the-loop. No auto-submit.")

if page == "Add Job":
    st.title("Add Job")
    url = st.text_input("Job URL")
    title = st.text_input("Title override")
    company = st.text_input("Company override")
    location = st.text_input("Location override")
    salary = st.text_input("Salary override")
    description = st.text_area("Raw job description", height=320)
    if st.button("Save job", type="primary"):
        if not description.strip():
            st.error("Job description is required.")
        else:
            job = build_job_from_input(description, url, title, company, location, salary)
            job_id = add_job(job)
            st.success(f"Saved job #{job_id}: {job.title} at {job.company}")

elif page == "Match Score":
    st.title("Match Score")
    row = selected_job()
    if row:
        job = to_job(row)
        preferences = load_preferences(PREFERENCES)
        fit = score_job(job, preferences)
        update_fit_score(job.id or row["id"], fit.score, fit.details)
        st.metric("Fit score", f"{fit.score}/100")
        st.json(fit.details)

elif page == "Tailor Resume":
    st.title("Tailor Resume")
    row = selected_job()
    if row:
        job = to_job(row)
        master_resume = read_text(MASTER_RESUME)
        tailored = tailor_resume(master_resume, job)
        save_resume(job.id or row["id"], tailored.summary, tailored.skills, tailored.bullets, tailored.missing_keywords)
        st.subheader("Tailored summary")
        st.write(tailored.summary)
        st.subheader("Matching skills")
        st.write(", ".join(tailored.skills) or "No direct keyword matches found.")
        st.subheader("Suggested bullets")
        for bullet in tailored.bullets:
            st.write(f"- {bullet}")
        st.subheader("Missing keywords")
        st.write(", ".join(tailored.missing_keywords) or "None")
        st.warning("Review manually. Do not add skills or experience that are not true.")

elif page == "Generate Messages":
    st.title("Generate Messages")
    row = selected_job()
    if row:
        job = to_job(row)
        tailored = tailor_resume(read_text(MASTER_RESUME), job)
        messages = {
            "Cover letter": cover_letter(job, tailored),
            "Recruiter LinkedIn message": linkedin_message(job),
            "Email application message": email_application_message(job),
            "Follow-up message": followup_message(job),
        }
        message_type = st.selectbox("Message type", list(messages))
        content = messages[message_type]
        st.text_area("Generated draft", value=content, height=300)
        if st.button("Save generated message"):
            if message_type == "Cover letter":
                save_cover_letter(job.id or row["id"], content)
            save_generated_answer(message_type, message_type, content, job.id or row["id"])
            st.success("Saved draft.")
        st.caption(clipboard_instruction("Use the text above only after reviewing it."))

elif page == "Application Tracker":
    st.title("Application Tracker")
    rows = latest_applications()
    st.dataframe(rows, use_container_width=True)
    row = selected_job()
    if row:
        status = st.selectbox("New status", APPLICATION_STATUSES)
        notes = st.text_area("Notes")
        if st.button("Update status"):
            set_application_status(row["id"], status, notes)
            st.success("Status updated.")

elif page == "Follow-ups":
    st.title("Follow-ups")
    rows = latest_applications()
    followups = [row for row in rows if row["status"] == "follow-up needed"]
    st.dataframe(followups, use_container_width=True)
    row = selected_job()
    if row:
        message = followup_message(to_job(row))
        st.text_area("Follow-up draft", value=message, height=220)

elif page == "Settings":
    st.title("Settings")
    st.write(f"Database: `{DB_PATH}`")
    st.subheader("Preferences")
    st.json(read_json(PREFERENCES, {}))
    st.subheader("Common answers")
    st.json(read_json(COMMON_ANSWERS, {}))
    st.subheader("Browser helper")
    enabled = st.checkbox("Enable browser helper for this session", value=False)
    use_playwright = st.checkbox("Use Playwright if installed", value=False)
    row = selected_job()
    if row and st.button("Open application URL"):
        st.info(open_application_url(row.get("url") or "", enabled=enabled, use_playwright=use_playwright))
    st.warning("Never auto-submit applications, bypass CAPTCHA, or automate LinkedIn/Indeed activity.")
