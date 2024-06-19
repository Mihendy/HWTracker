from django.test import TestCase

from main.models import Group
from users.models import User


def create_user(username, email, first_name,
                last_name='', group=None, password=None, is_editor=False, is_superuser=False):
    return User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        group=group,
        is_editor=is_editor,
        is_superuser=is_superuser,
        is_staff=is_superuser
    )


class TestUserModel(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='TestGroup')

    def test_create_user(self):
        user = create_user('testuser', 'testuser@example.com', 'USER',
                           group=self.group,
                           is_editor=True
                           )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.first_name, 'USER')
        self.assertEqual(user.group, self.group)
        self.assertTrue(user.is_editor)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.last_name, '')

    def test_user_str_representation(self):
        user = create_user(username='testuser', email='test@example.com', first_name='John', last_name='Doe')
        expected_output = 'test@example.com'
        self.assertEqual(str(user), expected_output)
