from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # just check title
        self.assertIn('TODO', self.browser.title)
        # self.fail 無論如何都會失敗並產生給定的訊息
        self.fail('Finish test.')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
