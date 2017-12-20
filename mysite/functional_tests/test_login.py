import time
from .base import FunctionalTest


class LoginTest(FunctionalTest):

    def test_login(self):
        """
        login test
        """
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()
        self.wait_for(lambda: self.assertRegex(self.browser.current_url, '/login/'))

        self.browser.find_element_by_name('username').send_keys("admin")
        time.sleep(1)
        self.browser.find_element_by_name('password').send_keys("1234qwer")
        time.sleep(1)
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()

        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.alert-success').text, 'Login successfully.'))
        time.sleep(1)

        """
        logout test
        """
        self.browser.find_element_by_id('logout').click()
        self.wait_for(lambda: self.assertRegex(self.browser.current_url, '/'))
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.alert-success').text, 'Logout successfully.'))
        time.sleep(1)
