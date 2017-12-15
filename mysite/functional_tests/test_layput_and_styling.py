from unittest import skip
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    # Dont test style I think.
    @skip
    def test_layout_and_styling(self):
        # AAA open the website of lists
        self.browser.get(self.live_server_url + '/lists/')
        self.browser.set_window_size(1024, 768)

        # input box style in center
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # AAA key something
        # input box style still in center
        inputbox.send_keys('test')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )
        self.fail('No style test.')
