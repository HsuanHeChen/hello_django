import time
from django.contrib.auth import get_user_model
from selenium.webdriver.common.keys import Keys
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
        # AAA login
        self.create_pre_authenticated_session()

        # AAA create item
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('AAA want to do sth1.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('AAA want to do sth1.'))
        self.get_item_input_box().send_keys('AAA want to do sth2.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('AAA want to do sth2.'))
        first_url = self.browser.current_url

        # AAA find a link named 'My List'
        self.browser.find_element_by_link_text('My Lists').click()

        # AAA get his Lists named by first list item.
        self.browser.find_element_by_link_text('AAA want to do sth1.').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_url))

        # AAA created the second list.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('AAA list 2')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('AAA list 2'))
        second_url = self.browser.current_url

        # 'AAA list 2' should be found in lists
        self.browser.find_element_by_link_text('My Lists').click()
        self.browser.find_element_by_link_text('AAA list 2').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_url))
        time.sleep(1)

        # AAA logout
        # My lists link should be disepear
        self.browser.find_element_by_id('logout').click()
        self.browser.get(self.server_url)
        self.assertEqual(self.browser.find_elements_by_link_text('My Lists'), [])
