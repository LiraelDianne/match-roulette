from django.test import TestCase

# Create your tests here.
from django.test import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(MySeleniumTests, cls).setUpClass()
        cls.selenium = WebDriver()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.selenium.quit()
        except AttributeError:
            pass
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):
        from selenium.webdriver.support.wait import WebDriverWait
        timeout = 2

        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.selenium.find_element_by_name("first_name")
        username_input.send_keys('firstname1')
        username_input = self.selenium.find_element_by_name("last_name")
        username_input.send_keys('lastname1')
        password_input = self.selenium.find_element_by_name("alias")
        password_input.send_keys('alias')
        password_input = self.selenium.find_element_by_name("email")
        password_input.send_keys('user1@emails.com')
        password_input = self.selenium.find_element_by_name("birthday")
        password_input.send_keys('1989-06-13')
        password_input = self.selenium.find_element_by_name("confirm_password")
        password_input.send_keys('Password')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('Password')

        self.selenium.find_element_by_xpath('//input[@value="Register"]').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.selenium.find_element_by_name("home-button").click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.selenium.find_element_by_name("test").click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.selenium.verifyTextPresent("newroom")
