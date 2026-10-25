import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.modals import ModalsPage


@pytest.fixture
def page(driver):
    return ModalsPage(driver).open()


@pytest.mark.positive
def test_modals_heading(page):
    assert page.heading() == 'Modals'


@pytest.mark.positive
def test_simple_button_visible(page):
    assert page.visible(By.XPATH, '//button[normalize-space()="Simple Modal"]').is_enabled()


@pytest.mark.positive
def test_form_button_visible(page):
    assert page.visible(By.XPATH, '//button[normalize-space()="Form Modal"]').is_enabled()


@pytest.mark.positive
def test_simple_modal_text(page):
    assert 'simple modal' in page.open_simple().text.lower()


@pytest.mark.positive
def test_form_modal_text(page):
    assert 'contact info' in page.open_form().text.lower()


@pytest.mark.positive
def test_simple_modal_can_close(page):
    page.open_simple()
    page.close_modal()
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[normalize-space(text())="Hi, I’m a simple modal."]'))


@pytest.mark.positive
def test_form_modal_can_close(page):
    page.open_form()
    page.close_modal()
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[contains(text(),"Please enter your contact info below.")]'))


@pytest.mark.positive
def test_simple_modal_can_be_reopened(page):
    page.open_simple()
    page.close_modal()
    assert page.open_simple().is_displayed()


@pytest.mark.negative
def test_modal_not_visible_initially(page):
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[normalize-space(text())="Hi, I’m a simple modal."]'))


@pytest.mark.negative
def test_form_not_visible_initially(page):
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[contains(text(),"Please enter your contact info below.")]'))


@pytest.mark.negative
def test_close_does_not_navigate_away(page):
    url = page.driver.current_url
    page.open_simple()
    page.close_modal()
    assert page.driver.current_url == url
