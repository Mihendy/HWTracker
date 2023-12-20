from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Group

class TestUserModel(TestCase):

    def setUp(self):
        self.group = Group.objects.create(name='Test Group')

    def create_user(self, username, password, email, group, is_editor=False, is_superuser=False):
        return get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email,
            group=group,
            is_editor=is_editor,
            is_superuser=is_superuser,
            is_staff=is_superuser
        ) 

    def test_create_user(self):
        user = self.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            group=self.group,
            is_editor=True
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.group, self.group)
        self.assertTrue(user.is_editor)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = self.create_user(
            username='adminuser',
            password='adminpassword',
            email='adminuser@example.com',
            group=self.group,
            is_superuser=True
        )
        self.assertEqual(superuser.username, 'adminuser')
        self.assertEqual(superuser.email, 'adminuser@example.com')
        self.assertEqual(superuser.group, self.group)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_user_str_representation(self):
        user = self.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            group=self.group
        )
        self.assertEqual(str(user), 'testuser')
