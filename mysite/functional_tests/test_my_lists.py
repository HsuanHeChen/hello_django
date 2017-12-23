import time
from django.contrib.auth import get_user_model
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

User = get_user_model()


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # AAA login
        self.create_pre_authenticated_session('aaa', '1234qwer', 'aaa@aaa.com')

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
        self.wait_for(lambda: self.browser.find_element_by_link_text('AAA list 2').click())
        time.sleep(5)
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_url))
        time.sleep(1)

        # AAA logout
        # My lists link should be disepear
        self.browser.find_element_by_id('logout').click()
        self.browser.get(self.server_url)
        self.assertEqual(self.browser.find_elements_by_link_text('My Lists'), [])
