from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .home_and_list_pages import HomePage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class ShareingTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):

        # AAA is a login user
        self.create_pre_authenticated_session('AAA', '1234qwer', 'aaa@mail.com')
        aaa_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(aaa_browser))

        # BBB is a login user
        bbb_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(bbb_browser))
        self.browser = bbb_browser
        self.create_pre_authenticated_session('BBB', '1234qwer', 'bbb@mail.com')

        # AAA go to add a list
        self.browser = aaa_browser
        list_page = HomePage(self).start_new_list('Get help')

        # there is a share btn
        share_box = list_page.get_share_box()
        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')

        # AAA share the list with bbb@gmail.com
        # reflesh and list is sharing with BBB
        list_page.share_list_with('bbb@mail.com')

        # BBB
        self.browser = bbb_browser
        HomePage(self).go_to_home_page().go_to_my_lists_page()

        # the share list's owner is aaa
        self.browser.find_element_by_link_text('Get help').click()
        self.wait_for(lambda: self.assertEqual(list_page.get_list_owner(), 'aaa@mail.com'))

        # BBB add item in this list
        list_page.add_new_item('Hi, AAA.')

        # AAA reflesh it and get the new item by BBB
        self.browser = aaa_browser
        self.browser.refresh()
        list_page.wait_for_new_item_in_list('Hi, AAA.')
