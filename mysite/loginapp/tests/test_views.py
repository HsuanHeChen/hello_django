from django.test import TestCase
from django.contrib.auth import get_user_model, SESSION_KEY
from mock import patch

User = get_user_model()


class LoginViewTest(TestCase):

    @patch('django.contrib.auth.authenticate')
    def test_calls_authentication_with_assertion_from_post(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/login/', {'username': 'AAA', 'password': 'aaaaaaaa'})
        mock_authenticate.assert_called_once_with(username='AAA', password='aaaaaaaa')

    @patch('django.contrib.auth.authenticate')
    def test_get_logged_in_session_if_authrnticate_returns_a_user(self, mock_authenticate):
        user = User.objects.create(email='aaa@b.com', username='AAA', password='aaaaaaaa')
        mock_authenticate.return_value = user
        self.client.post('/login/', {'username': 'AAA', 'password': 'aaaaaaaa'})
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    @patch('django.contrib.auth.authenticate')
    def test_does_not_get_logged_in_session_if_authrnticate_returns_none(self, mock_authenticate):
        mock_authenticate.return_value = None
        self.client.post('/login/', {'username': 'AAA', 'password': 'aaaaaaaa'})
        self.assertNotIn(SESSION_KEY, self.client.session)
