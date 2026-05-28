from src.models import Job, TailoredResume
from src.utils import read_json


def cover_letter(job: Job, tailored: TailoredResume) -> str:
    skills = ", ".join(tailored.skills[:6]) or "DevOps, cloud operations, and production support"
    return (
        f"Dear {job.company} team,\n\n"
        f"I am interested in the {job.title} role. My background aligns with the role through practical experience in "
        f"{skills}. I focus on reliable deployments, clear incident response, monitoring, troubleshooting, and continuous "
        "improvement through RCA and automation.\n\n"
        "I would welcome the opportunity to discuss how my experience can support your team.\n\n"
        "Regards,\nAshwini"
    )


def linkedin_message(job: Job) -> str:
    return (
        f"Hi, I saw the {job.title} role at {job.company} and wanted to reach out. "
        "My background is in DevOps, cloud, production support, monitoring, and incident response. "
        "I would appreciate the chance to connect or learn more about the role."
    )


def email_application_message(job: Job) -> str:
    return (
        f"Hello,\n\nI am applying for the {job.title} role at {job.company}. "
        "I have relevant experience in DevOps, cloud operations, CI/CD, monitoring, and production support. "
        "Please find my resume attached for your review.\n\nRegards,\nAshwini"
    )


def followup_message(job: Job) -> str:
    return (
        f"Hello,\n\nI wanted to follow up on my application for the {job.title} role at {job.company}. "
        "I remain interested in the opportunity and would be happy to provide any additional information.\n\n"
        "Regards,\nAshwini"
    )


def common_answers(path) -> dict:
    return read_json(path, {})
