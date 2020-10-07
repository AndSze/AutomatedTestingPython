# it will contain things that are identical for every page
from tests.acceptance.locators.base_page import BasePageLocators


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @property
    def url(self):
        return "http://127.0.0.1:5000"

    @property  # better approach for method inside a class that do not take any input arguments
    def title(self):
        return self.driver.find_element(*BasePageLocators.TITLE)  # tuple decomposition by the use of asterisk (*)

    @property
    def navigation(self):
        return self.driver.find_elements(*BasePageLocators.NAV_LINK)