FIELD_PATTERNS = {
    "name": ["full name", "name"],
    "email": ["email", "e-mail"],
    "phone": ["phone", "mobile"],
    "location": ["location", "city", "country"],
    "work_authorization": ["work authorization", "authorized to work", "eligible to work"],
    "sponsorship": ["sponsorship", "visa sponsorship", "require sponsorship"],
    "salary_expectation": ["salary", "compensation", "expected pay"],
    "notice_period": ["notice period", "start date", "available to start"],
    "relocation": ["relocation", "relocate"],
    "remote_hybrid_preference": ["remote", "hybrid", "onsite", "on-site"],
    "years_of_experience": ["years of experience", "experience"],
    "resume": ["resume", "cv"],
    "cover_letter": ["cover letter"],
}


def detect_likely_fields(text: str) -> list[str]:
    lowered = text.lower()
    detected = []
    for field, patterns in FIELD_PATTERNS.items():
        if any(pattern in lowered for pattern in patterns):
            detected.append(field)
    return detected
