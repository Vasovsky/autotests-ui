import re

import pytest
from playwright.sync_api import Page, expect


COURSES_URL = (
    "https://nikita-filonov.github.io/"
    "qa-automation-engineer-ui-course/#/courses"
)


@pytest.mark.courses
@pytest.mark.regression
def test_empty_courses_list(chromium_page_with_state: Page) -> None:
    page = chromium_page_with_state

    page.goto(COURSES_URL)

    expect(page).to_have_url(re.compile(r".*/#/courses"))

    courses_title = page.get_by_test_id(
        "courses-list-toolbar-title-text"
    )
    expect(courses_title).to_be_visible()
    expect(courses_title).to_have_text("Courses")

    empty_icon = page.get_by_test_id(
        "courses-list-empty-view-icon"
    )
    expect(empty_icon).to_be_visible()

    empty_title = page.get_by_test_id(
        "courses-list-empty-view-title-text"
    )
    expect(empty_title).to_be_visible()
    expect(empty_title).to_have_text("There is no results")

    empty_description = page.get_by_test_id(
        "courses-list-empty-view-description-text"
    )
    expect(empty_description).to_be_visible()
    expect(empty_description).to_have_text(
        "Results from the load test pipeline will be displayed here"
    )