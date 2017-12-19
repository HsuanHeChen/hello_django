from django.test import TestCase
from mock import patch


class LoginViewTest(TestCase):

    @patch('django.contrib.auth.authenticate')
    def test_calls_authentication_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/login', {'assertion': 'assert this'})
        mock_authenticate.assert_called_once_with(assertion='assert this')
