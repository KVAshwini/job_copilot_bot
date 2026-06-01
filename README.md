# Aura Job Copilot

Local-first job application copilot for job tracking, resume tailoring, fit scoring, and application messages.

This is a separate project from `aura-interview-engine` / `interview_bot`.

Long-term architecture:

- `aura-interview-engine`: realtime interview assistant
- `aura-job-copilot`: job application workflow dashboard
- `role_workspace.py`: branch UI for role/profession planning
- `aura-core`: future shared memory, LLM, resume, and profile module

## Features

- Streamlit dashboard
- SQLite database
- Add jobs from pasted URL and job description
- Rule-based fit score from 0-100
- Resume tailoring suggestions from `data/master_resume.md`
- Cover letter, recruiter message, email, and follow-up drafts
- Common application answer library
- Apply Assistant page for manual application packets
- Application status tracker
- Optional browser helper, disabled by default
- Local-first and no paid API required

## Install

```bash
cd aura-job-copilot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The default `app.py` dashboard remains the personal job workflow UI.

For the separate role/profession planning UI, run:

```bash
streamlit run role_workspace.py --server.port 8502
```

The role workspace uses:

```text
data/role_profiles.json
```

It covers target titles, core skills, resume focus areas, screening questions, and job-search terms for multiple roles.

## Initialize Database

The app initializes SQLite automatically. The database lives at:

```text
data/aura_job_copilot.db
```

## Safety Limitations

- Human-in-the-loop only.
- Does not auto-submit applications.
- Does not bypass CAPTCHA.
- Does not scrape or automate LinkedIn/Indeed activity.
- Does not mass apply or fill/submit forms automatically.
- Does not invent fake experience.
- Resume tailoring only suggests wording supported by `data/master_resume.md`.

## Apply Assistant Spike

The Apply Assistant is now part of the main job copilot dashboard. It uses saved jobs, `data/common_application_answers.json`, and optional profile fields typed in the UI to build a manual application packet.

The packet includes detected application fields, prepared answers, a readiness score, and missing-field warnings. You can save the packet and mark the job as applied only after you submit it yourself.

## Optional Browser Helper

The browser helper is disabled by default in `config/settings.yaml`. When enabled from the Settings page, it can open the application URL for manual review. If Playwright is installed and explicitly selected, it opens a visible browser page only.

It does not fill forms, submit applications, scrape job boards, bypass CAPTCHA, or automate LinkedIn/Indeed activity.

## Job Board Compliance

Use this tool for manual workflow support. Follow each job board's terms of service. For LinkedIn, Indeed, and similar platforms, do not use automation to scrape, mass apply, message, or bypass platform controls.

## Future Aura-Core Integration

Later, `aura-core` can own shared resume/profile memory, common LLM adapters, and reusable scoring utilities. This project currently keeps those pieces local under `data/` and `src/`.

## Tests

```bash
pytest
```
