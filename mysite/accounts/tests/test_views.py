from django.test import TestCase
from mock import patch


class LoginViewTest(TestCase):

    @patch('loginapp.views.authenticate')
    def test_calls_authentication_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/accounts/login')
