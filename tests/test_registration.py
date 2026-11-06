from uuid import uuid4

from playwright.sync_api import Playwright, expect


REGISTRATION_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/auth/registration"
)

DASHBOARD_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/dashboard"
)


def test_successful_registration(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    try:
        context = browser.new_context()
        page = context.new_page()

        suffix = uuid4().hex[:8]

        page.goto(REGISTRATION_URL)

        page.get_by_test_id(
            "registration-form-email-input"
        ).locator("input").fill(f"user_{suffix}@example.com")

        page.get_by_test_id(
            "registration-form-username-input"
        ).locator("input").fill(f"user_{suffix}")

        page.get_by_test_id(
            "registration-form-password-input"
        ).locator("input").fill("password")

        page.get_by_test_id(
            "registration-page-registration-button"
        ).click()

        expect(page).to_have_url(DASHBOARD_URL)
    finally:
        browser.close()