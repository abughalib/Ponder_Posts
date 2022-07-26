from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User

from users.models import User


class UserCreationTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username='tester',
            email='test_user@example.com',
            password='top_secret_password'
        )
        self.assertEqual(user is not None, True)
