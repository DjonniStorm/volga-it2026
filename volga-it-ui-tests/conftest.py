import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


@pytest.fixture
def driver(request):
    browser = os.getenv('BROWSER', 'chrome').lower()
    if browser == 'chrome':
        options = ChromeOptions()
        if os.getenv('HEADLESS', '1') == '1':
            options.add_argument('--headless=new')
        options.add_argument('--window-size=1440,1000')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        instance = webdriver.Chrome(options=options)
    elif browser == 'firefox':
        options = FirefoxOptions()
        if os.getenv('HEADLESS', '1') == '1':
            options.add_argument('-headless')
        instance = webdriver.Firefox(options=options)
        instance.set_window_size(1440, 1000)
    else:
        raise ValueError('BROWSER must be chrome or firefox')

    instance.set_page_load_timeout(30)
    yield instance
    if request.node.rep_call.failed:
        try:
            allure.attach(instance.get_screenshot_as_png(), name='Failure screenshot', attachment_type=allure.attachment_type.PNG)
            allure.attach(instance.page_source, name='Page source', attachment_type=allure.attachment_type.HTML)
        except Exception:
            pass
    instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f'rep_{report.when}', report)
