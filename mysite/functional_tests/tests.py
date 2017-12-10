from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('li')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Who open the website
        # self.browser.get('http://localhost:8000/lists/')
        self.browser.get(self.live_server_url+'/lists/')

        # there are title and h1
        self.assertIn('TODO', self.browser.title)
        h1 = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO', h1)

        # there is a input box with placeholder
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a TODO item.')

        # enter to do list in the input box and send it
        inputbox.send_keys('[FT] I want to do sth1.')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # find it on page
        self.check_for_row_in_list_table('[FT] I want to do sth1.')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('[FT] I want to do sth2.')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)

        # find they on page
        self.check_for_row_in_list_table('[FT] I want to do sth2.')
        self.check_for_row_in_list_table('[FT] I want to do sth1.')

        # self.fail 無論如何都會失敗並產生給定的訊息
        self.fail('Finish test.')


# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
