import sys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from django.contrib.auth import get_user_model

User = get_user_model()
MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url + '/lists/'

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url + '/lists/':
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create_user(
            username='admin',
            password='1234qwer',
            email='admin@example.com'
        )
        # 不可靠
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('li')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')

    def wait_for(self, fn):
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def create_pre_authenticated_session(self, name, pw, email):
        User.objects.create_user(
            username=name,
            password=pw,
            email=email,
        )
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()
        self.browser.find_element_by_name('username').send_keys(name)
        self.browser.find_element_by_name('password').send_keys(pw)
        self.browser.find_element_by_xpath('//input[@type="submit"]').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_element_by_css_selector('.alert-success').text, 'Login successfully.'))
