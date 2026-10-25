from selenium.webdriver.common.by import By
from pages.base import BasePage


class FormFieldsPage(BasePage):
    path = '/form-fields/'

    def tools(self):
        group = self.driver.find_element(By.XPATH, '//*[contains(translate(normalize-space(text()),"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"automation tools")][1]')
        values = self.driver.execute_script('''
            const n=arguments[0];
            let root=n.closest('fieldset, .wp-block-group, form') || n.parentElement;
            if(root.tagName.toLowerCase()==='form') root=n.parentElement;
            const options=[...root.querySelectorAll('label,li')].map(e=>e.textContent.trim()).filter(Boolean);
            return options;
        ''', group)
        names = [v for v in values if any(t in v.lower() for t in ('selenium','playwright','cypress','appium','katalon'))]
        if len(names) < 5:
            names = self.driver.execute_script('''
                let n=arguments[0], result=[];
                for(let e=n.nextElementSibling,i=0;e&&i<8;e=e.nextElementSibling,i++) {
                  result.push(...[...e.querySelectorAll('li,label')].map(n=>n.textContent.trim()));
                }
                return result.filter(Boolean);
            ''', group)
        if len(names) < 5:
            raise AssertionError(f'Could not extract 5 automation tools via Selenium DOM: {names}')
        return names[:5]

    def message(self):
        return self.visible(By.XPATH, '//textarea[not(ancestor::*[contains(@class,"modal")])] | //textarea[@id="message"]')
