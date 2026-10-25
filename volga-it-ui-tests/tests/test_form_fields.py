import allure
from pages.form_fields import FormFieldsPage


@allure.title('Message is built dynamically from Automation Tools with Selenium')
def test_message_contains_tools_collected_from_dom(driver):
    page = FormFieldsPage(driver).open()
    with allure.step('Get tool names from Automation Tools section using Selenium'):
        tools = page.tools()
    with allure.step('Join extracted tools using commas'):
        message = ', '.join(tools)
    with allure.step('Fill Message field with the extracted list'):
        page.message().send_keys(message)
    assert page.message().get_attribute('value') == message
    assert len(tools) == 5
