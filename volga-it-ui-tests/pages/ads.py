from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base import BasePage


class AdsPage(BasePage):
    path = '/ads/'

    def ad(self, timeout=18):
        return WebDriverWait(self.driver, timeout).until(
            lambda d: next((e for e in d.find_elements(By.XPATH, '//*[normalize-space(text())="I am an ad."]') if e.is_displayed()), False)
        )

    def close(self):
        ad = self.ad()
        modal = self.driver.execute_script('return arguments[0].closest("[role=dialog],.modal,.pum-container,.remodal")', ad)
        if modal is None:
            modal = ad.find_element(By.XPATH, './ancestor::*[.//button[contains(normalize-space(.),"×")]][1]')
        buttons = [b for b in modal.find_elements(By.XPATH, './/button[contains(normalize-space(.),"×") or contains(@class,"close")]') if b.is_displayed()]
        if not buttons:
            raise AssertionError('Visible ad has no close button')
        buttons[-1].click()
        WebDriverWait(self.driver, 8).until(EC.invisibility_of_element(ad))
