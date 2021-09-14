import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Web:
    def __init__(self):
        self.driver = webdriver.Chrome(r"C:\Python programs\Selenium_python\chromedriver_win32\chromedriver.exe")

    def get(self, url):
        self.driver.get(url)

    def get_element_by_id(self, name):
        return self.driver.find_element_by_id(name)

    def get_element_by_class(self, name):
        return self.driver.find_element_by_class_name(name)

    def get_elements_by_class(self, name):
        return self.driver.find_elements_by_class_name(name)

    def get_element_by_css_selector(self, name):
        return self.driver.find_element_by_css_selector(name)

    def get_element_by_xpath(self, name):
        return self.driver.find_element_by_xpath(name)

    def get_elements_by_xpath(self, name):
        return self.driver.find_elements_by_xpath(name)

    def get_elements_by_name(self, name):
        return self.driver.find_elements_by_name(name)

    def get_element_by_link_text(self, name):
        return self.driver.find_element_by_partial_link_text(name)