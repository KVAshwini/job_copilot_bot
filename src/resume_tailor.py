from src.jd_parser import extract_keywords
from src.models import Job, TailoredResume
from src.utils import keyword_hits


def tailor_resume(master_resume: str, job: Job) -> TailoredResume:
    jd_keywords = extract_keywords(job.description)
    resume_matches = keyword_hits(master_resume, jd_keywords)
    missing = [keyword for keyword in jd_keywords if keyword not in resume_matches]
    top_skills = resume_matches[:12]
    role_focus = ", ".join(top_skills[:5]) or "production support, DevOps, and cloud operations"

    summary = (
        f"DevOps and production support engineer with hands-on experience across {role_focus}. "
        f"Prepared to support {job.company}'s {job.title} role by emphasizing proven troubleshooting, "
        "monitoring, deployment, and incident-response experience from the master resume."
    )
    bullets = [
        f"Emphasize production troubleshooting experience relevant to {job.title}, especially around {role_focus}.",
        "Highlight incident response, monitoring, RCA, deployment support, and cross-team coordination.",
        "Use only tools and responsibilities already present in the master resume; do not add unverified experience.",
    ]
    if missing:
        bullets.append("Add truthful context for matching keywords only if the master resume already supports them.")

    return TailoredResume(summary=summary, skills=top_skills, bullets=bullets, missing_keywords=missing)
