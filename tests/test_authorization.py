import pytest
from playwright.sync_api import Page, expect


LOGIN_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/auth/login"
)


@pytest.mark.regression
@pytest.mark.authorization
@pytest.mark.parametrize(
    "email,password",
    [
        pytest.param(
            "user.name@gmail.com", "password", id="invalid-credentials"
        ),
        pytest.param("user.name@gmail.com", "  ", id="blank-password"),
        pytest.param("  ", "password", id="blank-email"),
    ],
)
def test_wrong_email_or_password_authorization(
    chromium_page: Page, email: str, password: str
) -> None:
    chromium_page.goto(LOGIN_URL)

    email_input = chromium_page.get_by_test_id("login-form-email-input")
    email_input.locator("input").fill(email)

    password_input = chromium_page.get_by_test_id("login-form-password-input")
    password_input.locator("input").fill(password)

    chromium_page.get_by_test_id("login-page-login-button").click()

    alert = chromium_page.get_by_test_id(
        "login-page-wrong-email-or-password-alert"
    )
    expect(alert).to_be_visible()
    expect(alert).to_have_text("Wrong email or password")
