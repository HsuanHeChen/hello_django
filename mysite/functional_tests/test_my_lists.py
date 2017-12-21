import time
from django.contrib.auth import get_user_model
from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self):
        User.objects.create_user(
            username='aaa',
            password='1234qwer',
            email='aaa@example.com'
        )
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()
        self.browser.find_element_by_name('username').send_keys("aaa")
        self.browser.find_element_by_name('password').send_keys("1234qwer")
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.alert-success').text, 'Login successfully.'))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        self.create_pre_authenticated_session()
        self.browser.get(self.server_url)
        self.wait_for(lambda: self.assertIn('aaa', self.browser.find_element_by_id('header-nav').text))
        time.sleep(1)
