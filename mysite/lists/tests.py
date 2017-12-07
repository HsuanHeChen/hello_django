from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from .views import home_page

# Create your tests here.


class ListPageTest(TestCase):

    def test_list_view_url_to_list_view(self):
        found = resolve('/lists/')
        self.assertEqual(found.func, home_page)

    def test_list_view_returns_correct_html(self):
        request = HttpRequest()
        res = home_page(request)
        self.assertTrue(res.content.startswith(b'<html>'))
        self.assertIn(b'<title>TODO lists</title>', res.content)
        self.assertTrue(res.content.endswith(b'</html>'))
