from django.test import TestCase
from users.models import User
from main.models import Group, Task, GroupAdmin
from datetime import datetime, timedelta
from django.utils import timezone
from random import shuffle


class TestGroupModel(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            email='user2@example.com'
        )

    def test_group_str_representation(self):
        group_name = 'Test Group'
        group = Group.objects.create(name=group_name)
        self.assertEqual(str(group), group_name)

    def test_group_meta_ordering(self):
        group_names = ['FT-201', 'FT-202', 'FT-203']
        shuffle(group_names)
        for name in group_names:
            Group.objects.create(name=name)

        expected_order = sorted(group_names)
        queryset = Group.objects.all()
        self.assertQuerysetEqual(queryset, expected_order, lambda x: x.name)

    def test_group_user_count(self):
        group = Group.objects.create(name='Test Group')
        group.users.add(self.user1, self.user2)
        group.save()

        admin_instance = GroupAdmin(model=Group, admin_site=None)
        user_count = admin_instance.get_user_count(group)

        self.assertEqual(user_count, 2)


class TestTaskModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(name='Test Group')
        self.user1 = User.objects.create_user(
            username='user1',
            password='password1',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='password2',
            email='user2@example.com'
        )

    def create_task(self, subject='Test Subject', topic='Test Topic', description='Test Description', due_date=None):
        if due_date is None:
            due_date = timezone.now() + timezone.timedelta(days=7)
        return Task.objects.create(
            subject=subject,
            topic=topic,
            description=description,
            due_date=due_date,
            group=self.group
        )

    def test_task_str_representation(self):
        task_data = {
            'subject': 'Test Subject',
            'topic': 'Test Topic',
            'description': 'Test Description',
            'due_date': datetime.now() + timedelta(days=7),
        }
        task = self.create_task(**task_data)
        expected_str = f'{task_data["subject"]} - {task_data["topic"]}'
        self.assertEqual(str(task), expected_str)

    def test_task_is_completed_by_user(self):
        task = self.create_task()
        self.assertFalse(task.is_completed_by_user(self.user))
        task.completed_by.add(self.user)
        self.assertTrue(task.is_completed_by_user(self.user))

    def test_task_meta_ordering(self):
        task_due_dates = [
            timezone.now() + timezone.timedelta(days=i) for i in range(3)
        ]

        for due_date in task_due_dates:
            self.create_task(due_date=due_date)

        expected_order = sorted(task_due_dates)
        expected_order = [date.replace(microsecond=0) for date in expected_order]

        queryset = Task.objects.all()
        queryset = [task.due_date.replace(microsecond=0) for task in queryset]

        self.assertQuerysetEqual(queryset, expected_order, lambda x: x)

    def test_task_is_completed_by_user_with_multiple_users(self):
        task = self.create_task()
        task.completed_by.add(self.user1)
        task.save()

        self.assertTrue(task.is_completed_by_user(self.user1))
        self.assertFalse(task.is_completed_by_user(self.user2))

    def test_task_completed_by_user_count(self):
        task = self.create_task()
        task.completed_by.add(self.user1, self.user2)
        task.save()

        self.assertEqual(task.completed_by.count(), 2)
