from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ListsTestCase(TestCase):

    def init_owner(self):
        return User.objects.create_user(
            username='aaa',
            password='1234qwer',
            email='aaa@example.com'
        )
