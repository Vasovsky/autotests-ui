import re
from uuid import uuid4

from playwright.sync_api import expect, sync_playwright


REGISTRATION_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/auth/registration"
)

COURSES_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/courses"
)


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)

    # Первая сессия браузера
    context = browser.new_context()
    page = context.new_page()

    # Случайные данные, чтобы не было конфликтов
    suffix = uuid4().hex[:8]
    email = f"student_{suffix}@example.com"
    username = f"student_{suffix}"
    password = "qwerty123"

    # 1. Открываем регистрацию
    page.goto(REGISTRATION_URL)

    # 2. Заполняем форму
    page.get_by_test_id("registration-form-email-input").fill(email)
    page.get_by_test_id("registration-form-username-input").fill(username)
    page.get_by_test_id("registration-form-password-input").fill(password)

    page.get_by_test_id(
        "registration-page-registration-button"
    ).click()

    # Проверяем успешную регистрацию
    expect(page).to_have_url(re.compile(r".*/#/dashboard"))

    # 3. Сохраняем состояние браузера
    storage_state = context.storage_state()

    # Закрываем первую сессию
    context.close()

    # 4. Создаём НОВУЮ сессию с сохранённым состоянием
    authorized_context = browser.new_context(
        storage_state=storage_state
    )

    authorized_page = authorized_context.new_page()

    # 5. Открываем Courses без повторной авторизации
    authorized_page.goto(COURSES_URL)

    expect(authorized_page).to_have_url(
        re.compile(r".*/#/courses")
    )

    # 6. Проверяем заголовок Courses
    courses_title = authorized_page.get_by_test_id(
        "courses-list-toolbar-title-text"
    )

    expect(courses_title).to_be_visible()
    expect(courses_title).to_have_text("Courses")

    # 7. Проверяем "There is no results"
    empty_title = authorized_page.get_by_test_id(
        "courses-list-empty-view-title-text"
    )

    expect(empty_title).to_be_visible()
    expect(empty_title).to_have_text(
        "There is no results"
    )

    # 8. Проверяем иконку пустого блока
    empty_icon = authorized_page.get_by_test_id(
        "courses-list-empty-view-icon"
    )

    expect(empty_icon).to_be_visible()

    # 9. Проверяем описание
    empty_description = authorized_page.get_by_test_id(
        "courses-list-empty-view-description-text"
    )

    expect(empty_description).to_be_visible()
    expect(empty_description).to_have_text(
        "Results from the load test pipeline will be displayed here"
    )

    print("Все проверки успешно пройдены.")

    authorized_context.close()
    browser.close()