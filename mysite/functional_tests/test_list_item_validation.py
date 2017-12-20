import time
from unittest import skip
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    # skip: the required input auto stop user send enter.
    @skip
    def test_cant_add_empty_item(self):
        # AAA open the website of lists
        self.browser.get(self.server_url)

        # inputbox submit with empty
        self.get_item_input_box().send_keys('\n')
        # page reload and got a message - no empty item
        error = self.browser.find_element_by_css_selector('.alert-warning')
        self.assertEqual(error.text, 'You cannot have an empty list item.')

        # enter something in the input box and send it, and it's working
        self.get_item_input_box().send_keys('Buy anything.\n')
        self.check_for_row_in_list_table('Buy anything.')

        self.fail('Write test.')

    def test_cant_add_duplicate_items(self):
        # AAA open the website of lists and sent 'taiwan'
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('Taiwan.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.check_for_row_in_list_table('Taiwan.'))

        # AAA sent 'taiwan' again
        self.get_item_input_box().send_keys('Taiwan.')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # page reload and got a message - no duplicate item
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.alert-warning').text,
            "You have already got this."
        ))

    @skip
    def test_error_messages_are_cleared_on_input(self):
        # AAA open the website of lists
        self.browser.get(self.server_url)
        # inputbox submit with empty and get a .has-error element from js
        self.get_item_input_box().send_keys(Keys.ENTER)
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertTrue(error.is_displayed())

        # input sth. and the .has-error should be gone
        self.get_item_input_box().send_keys('aaa')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertFalse(error.is_displayed())
