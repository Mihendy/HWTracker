from datetime import datetime

from django.test import TestCase

from main.forms import TaskForm
from main.models import Group
from main.validators import validate_extended_slug
from users.models import User


class TaskFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='email@mail.com')
        self.group = Group.objects.create(name='Test Group')
        self.form_data = {
            'subject': 'Test Subject',
            'topic': 'Test Topic',
            'description': 'Test Description',
            'due_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        }

    def test_valid_form_data(self):
        self.form_data['group'] = self.group.id
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = TaskForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)

    def test_invalid_due_date(self):
        self.form_data['group'] = self.group.id
        self.form_data['due_date'] = 'invalid_date_format'
        form = TaskForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_custom_validator(self):
        self.form_data['group'] = self.group.id
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())

        self.form_data['other_group'] = 'Invalid@Group'
        form = TaskForm(data=self.form_data)
        form.fields['other_group'].validators.append(validate_extended_slug)
        self.assertFalse(form.is_valid())
        self.assertIn('other_group', form.errors)

    def test_successful_task_creation(self):
        self.form_data['group'] = self.group.id
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_due_date_format(self):
        self.form_data['group'] = self.group.id
        self.form_data['due_date'] = 'invalid_date_format'
        form = TaskForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)

    def test_successful_task_creation_with_other_group(self):
        self.form_data['group'] = 'other'
        self.form_data['other_group'] = 'New-Group'
        form = TaskForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_other_group_name(self):
        self.form_data['group'] = 'other'
        self.form_data['other_group'] = 'Invalid,Group'
        form = TaskForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('other_group', form.errors)

    def test_missing_group_selection(self):
        form_data = self.form_data.copy()
        form_data.pop('group', None)
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('group', form.errors)