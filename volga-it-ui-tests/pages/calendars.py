from selenium.webdriver.common.by import By
from pages.base import BasePage


class CalendarsPage(BasePage):
    path = '/calendars/'

    @property
    def field(self):
        return self.visible(By.CSS_SELECTOR, 'input[type="date"]')

    def set_date(self, value):
        field = self.field
        self.driver.execute_script('arguments[0].value=arguments[1];arguments[0].dispatchEvent(new Event("input",{bubbles:true}));arguments[0].dispatchEvent(new Event("change",{bubbles:true}));', field, value)

    def submit(self):
        self.click(By.XPATH, '//main//button[normalize-space()="Submit"] | //article//button[normalize-space()="Submit"] | //input[@type="submit" and not(ancestor::*[contains(@class,"modal")])]')
