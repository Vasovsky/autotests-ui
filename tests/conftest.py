import re
from collections.abc import Iterator
from uuid import uuid4

import pytest
from playwright.sync_api import Page, Playwright, expect


REGISTRATION_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/auth/registration"
)


@pytest.fixture
def chromium_page(playwright: Playwright) -> Iterator[Page]:
    browser = playwright.chromium.launch(headless=False)
    try:
        yield browser.new_page()
    finally:
        browser.close()


@pytest.fixture(scope="session")
def initialize_browser_state(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)

    try:
        context = browser.new_context()

        try:
            page = context.new_page()

            suffix = uuid4().hex[:8]
            email = f"student_{suffix}@example.com"
            username = f"student_{suffix}"
            password = "qwerty123"

            page.goto(REGISTRATION_URL)

            page.get_by_test_id(
                "registration-form-email-input"
            ).locator("input").fill(email)

            page.get_by_test_id(
                "registration-form-username-input"
            ).locator("input").fill(username)

            page.get_by_test_id(
                "registration-form-password-input"
            ).locator("input").fill(password)

            page.get_by_test_id(
                "registration-page-registration-button"
            ).click()

            expect(page).to_have_url(re.compile(r".*/#/dashboard"))

            context.storage_state(path="browser-state.json")
        finally:
            context.close()
    finally:
        browser.close()


@pytest.fixture(scope="function")
def chromium_page_with_state(
    initialize_browser_state,
    playwright: Playwright,
) -> Iterator[Page]:
    browser = playwright.chromium.launch(headless=False)

    try:
        context = browser.new_context(
            storage_state="browser-state.json"
        )

        try:
            page = context.new_page()
            yield page
        finally:
            context.close()
    finally:
        browser.close()
