from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def xtest_cant_add_empty_item(self):
        # AAA open the website of lists
        self.browser.get(self.server_url + '/lists/')

        # inputbox submit with empty
        self.get_item_input_box().send_keys('\n')
        # page reload and got a message - no empty item
        error = self.browser.find_element_by_css_selector('.alert-warning')
        self.assertEqual(error.text, 'You cannot have an empty list item.')

        # enter something in the input box and send it, and it's working
        self.get_item_input_box().send_keys('Buy anything.\n')
        self.check_for_row_in_list_table('Buy anything.')

        self.fail('Write test.')
