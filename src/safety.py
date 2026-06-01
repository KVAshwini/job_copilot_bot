BLOCKED_ACTIONS = {
    "auto_submit_applications": False,
    "bypass_captcha": False,
    "automate_linkedin_indeed": False,
    "mass_apply": False,
    "invent_experience": False,
}


def safety_summary() -> list[str]:
    return [
        "Manual review is required before every application.",
        "The assistant does not submit applications.",
        "The assistant does not bypass CAPTCHA.",
        "The assistant does not automate LinkedIn or Indeed.",
        "Generated content must be verified against the real resume/profile.",
    ]


def can_auto_submit() -> bool:
    return False
