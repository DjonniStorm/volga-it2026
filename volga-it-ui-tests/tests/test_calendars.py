import pytest
import allure
from selenium.webdriver.common.by import By
from pages.calendars import CalendarsPage


@pytest.fixture
def page(driver):
    return CalendarsPage(driver).open()


@pytest.mark.positive
def test_calendar_heading(page):
    assert page.heading() == 'Calendars'


@pytest.mark.positive
def test_calendar_has_date_control(page):
    assert page.field.is_displayed()


@pytest.mark.positive
def test_calendar_date_is_editable(page):
    assert page.field.is_enabled()


@pytest.mark.positive
def test_calendar_submit_control(page):
    assert any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//button[normalize-space()="Submit"] | //input[@type="submit"]'))


@pytest.mark.positive
@pytest.mark.parametrize('value', ['2024-01-01', '2024-02-29', '2025-12-31', '2026-06-15'])
def test_calendar_accepts_valid_date(page, value):
    with allure.step(f'Select supported ISO date {value}'):
        page.set_date(value)
    assert page.field.get_attribute('value') == value


@pytest.mark.negative
@pytest.mark.parametrize('value', ['2025-02-30', '2025-13-01', 'not-a-date'])
def test_calendar_rejects_invalid_native_date(page, value):
    page.set_date(value)
    assert page.field.get_attribute('value') != value
