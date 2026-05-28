import webbrowser


def open_application_url(url: str, enabled: bool = False, use_playwright: bool = False) -> str:
    if not enabled:
        return "Browser helper is disabled in settings."
    if not url:
        return "No URL available."
    if use_playwright:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            webbrowser.open(url)
            return "Playwright is not installed. Opened URL in the default browser instead."

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
        return "Opened application URL with Playwright. Review and submit manually."
    webbrowser.open(url)
    return "Opened application URL. Review and submit manually."


def clipboard_instruction(text: str) -> str:
    return (
        "Copy this prepared answer manually into the application form. "
        "Aura Job Copilot never auto-submits applications and never bypasses CAPTCHA.\n\n"
        + text
    )
