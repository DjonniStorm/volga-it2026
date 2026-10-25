import pytest
from selenium.webdriver.common.by import By
from pages.ads import AdsPage


@pytest.fixture
def page(driver):
    return AdsPage(driver).open()


@pytest.mark.positive
def test_ads_heading(page):
    assert page.heading() == 'Ads'


@pytest.mark.positive
def test_ads_description(page):
    assert 'An ad will appear' in page.body()


@pytest.mark.positive
def test_ad_appears(page):
    assert page.ad().is_displayed()


@pytest.mark.positive
def test_ad_content(page):
    assert page.ad().text.strip() == 'I am an ad.'


@pytest.mark.positive
def test_ad_can_be_closed(page):
    page.close()
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[normalize-space(text())="I am an ad."]'))


@pytest.mark.positive
def test_ad_close_keeps_page(page):
    current = page.driver.current_url
    page.close()
    assert page.driver.current_url == current


@pytest.mark.positive
def test_page_heading_remains_after_ad_close(page):
    page.close()
    assert page.heading() == 'Ads'


@pytest.mark.positive
def test_page_text_remains_after_ad_close(page):
    page.close()
    assert 'content providers' in page.body()


@pytest.mark.negative
def test_ad_is_not_visible_after_close(page):
    page.close()
    assert not any(e.is_displayed() for e in page.driver.find_elements(By.XPATH, '//*[normalize-space(text())="I am an ad."]'))


@pytest.mark.negative
def test_close_does_not_remove_heading(page):
    page.close()
    assert page.driver.find_element(By.TAG_NAME, 'h1').is_displayed()


@pytest.mark.negative
def test_close_does_not_create_another_window(page):
    original = len(page.driver.window_handles)
    page.close()
    assert len(page.driver.window_handles) == original
