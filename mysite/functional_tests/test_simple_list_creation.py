import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # AAA open the website of lists
        self.browser.get(self.server_url + '/lists/')

        # there are title and h1
        self.assertIn('TODO', self.browser.title)
        h1 = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('TODO', h1)

        # there is a input box with placeholder
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a TODO item.')

        # enter to do list in the input box and send it
        inputbox.send_keys('[FT] AAA want to do sth1.')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # redirect to lists#show
        aaa_list_url = self.browser.current_url
        self.assertRegex(aaa_list_url, '/lists/.+')

        # find it on page
        self.check_for_row_in_list_table('[FT] AAA want to do sth1.')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('[FT] AAA want to do sth2.')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # find they on page
        self.check_for_row_in_list_table('[FT] AAA want to do sth2.')
        self.check_for_row_in_list_table('[FT] AAA want to do sth1.')

        # BBB open the website
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url + '/lists/')

        # There are no AAA's lists.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('[FT] AAA want to do sth2.', page_text)
        self.assertNotIn('[FT] AAA want to do sth1.', page_text)

        # BBB enter list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('[FT] BBB want to do sth1.')
        inputbox.send_keys(Keys.ENTER)

        bbb_list_url = self.browser.current_url
        self.assertRegex(aaa_list_url, '/lists/.+')
        self.assertNotEqual(aaa_list_url, bbb_list_url)

        # self.fail 無論如何都會失敗並產生給定的訊息
        # self.fail('Finish test.')
