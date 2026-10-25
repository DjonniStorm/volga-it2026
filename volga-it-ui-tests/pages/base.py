import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE = 'https://practice-automation.com'


class BasePage:
    path = '/'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)

    @allure.step('Open page {self.path}')
    def open(self):
        self.driver.get(BASE + self.path)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h1')))
        return self

    def heading(self):
        return self.driver.find_element(By.TAG_NAME, 'h1').text.strip()

    def visible(self, by, selector):
        return self.wait.until(EC.visibility_of_element_located((by, selector)))

    def click(self, by, selector):
        self.wait.until(EC.element_to_be_clickable((by, selector))).click()

    def body(self):
        return self.driver.find_element(By.TAG_NAME, 'body').text
