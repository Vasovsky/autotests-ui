from playwright.sync_api import sync_playwright, expect


REGISTRATION_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/auth/registration"
)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    # 1. Открываем страницу регистрации.
    page.goto(REGISTRATION_URL)

    # 2. Находим кнопку Registration и проверяем,
    #    что до заполнения формы она disabled.
    registration_button = page.get_by_test_id(
        "registration-page-registration-button"
    )
    expect(registration_button).to_be_disabled()

    # 3. Заполняем форму регистрации.
    email_input = page.get_by_test_id(
        "registration-form-email-input"
    ).locator("input")
    username_input = page.get_by_test_id(
        "registration-form-username-input"
    ).locator("input")
    password_input = page.get_by_test_id(
        "registration-form-password-input"
    ).locator("input")

    email_input.fill("user.name@gmail.com")
    username_input.fill("username")
    password_input.fill("password")

    # 4. После заполнения формы кнопка должна стать enabled.
    expect(registration_button).to_be_enabled()

    browser.close()