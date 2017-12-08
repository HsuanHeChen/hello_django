from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Who open the website
        self.browser.get('http://localhost:8000/lists/')

        # there are title and h1
        self.assertIn('TODO', self.browser.title)
        h1 = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO', h1)

        # there is a input box with placeholder
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a TODO item.')

        # enter to do list in the input box and send it
        inputbox.send_keys('I want to do sth.')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == 'I want to do sth.' for row in rows))


        # self.fail 無論如何都會失敗並產生給定的訊息
        self.fail('Finish test.')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
