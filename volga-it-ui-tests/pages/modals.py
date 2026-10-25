from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base import BasePage


class ModalsPage(BasePage):
    path = '/modals/'

    def open_simple(self):
        self.click(By.XPATH, '//button[normalize-space()="Simple Modal"]')
        return self.visible(By.XPATH, '//*[contains(normalize-space(.),"Hi, I’m a simple modal.") and (self::p or self::div)][not(.//*[contains(normalize-space(.),"Hi, I’m a simple modal.")])]')

    def open_form(self):
        self.click(By.XPATH, '//button[normalize-space()="Form Modal"]')
        return self.visible(By.XPATH, '//*[contains(normalize-space(.),"Please enter your contact info below.") and (self::p or self::div)][not(.//*[contains(normalize-space(.),"Please enter your contact info below.")])]')

    def active_modal(self):
        candidates = self.driver.find_elements(By.CSS_SELECTOR, '[role="dialog"], .modal, .pum-container, .remodal')
        visible = [e for e in candidates if e.is_displayed() and ('modal' in e.text.lower() or 'contact info' in e.text.lower())]
        return min(visible, key=lambda e: len(e.text)) if visible else None

    def close_modal(self):
        modal = self.active_modal()
        if modal:
            buttons = modal.find_elements(By.XPATH, './/button[contains(normalize-space(.),"×") or contains(@class,"close")]')
            buttons = [b for b in buttons if b.is_displayed()]
            if buttons:
                buttons[-1].click()
                self.wait.until(EC.invisibility_of_element(modal))
                return
        self.click(By.XPATH, '(//button[contains(normalize-space(.),"×") and not(ancestor::*[@aria-hidden="true"])])[last()]')
