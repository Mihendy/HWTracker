from django.test import Client, TestCase
from django.urls import reverse

from main.models import Group, Task
from users.models import User


class TestViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.force_login(self.user)
        self.index_url = reverse('index')
        self.student_url = reverse('student')

        self.group = Group.objects.create(name='Test_Group')
        self.task_data = {
            'subject': 'Test Subject',
            'topic': 'Test Topic',
            'description': 'Test Description',
            'due_date': '2023-12-31T23:59:59',
            'group': self.group
        }
        self.task = Task.objects.create(**self.task_data)

    def set_user_editor_role(self, is_editor=True):
        self.user.is_editor = is_editor
        self.user.save()

    def test_index_GET(self):
        response = self.client.get(self.index_url)
        print(response)
        self.assertEquals(response.status_code, 302)

    def test_student_GET(self):
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/student.html')

    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_add_task_form_GET(self):
        response = self.client.get(reverse('taskform'))
        self.assertEqual(response.status_code, 403)

        self.set_user_editor_role(True)
        response = self.client.get(reverse('taskform'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'main/add_task_form.html')

    def test_add_task_form_POST(self):
        self.set_user_editor_role(True)

        response = self.client.post(reverse('taskform'), self.task_data)
        self.assertEqual(response.status_code, 200)

    def test_edit_task_form_GET(self):
        self.set_user_editor_role(True)

        response = self.client.get(reverse('edit_task_form', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'main/add_task_form.html')

    def test_edit_task_form_POST(self):
        self.set_user_editor_role(True)

        updated_data = {
            'subject': 'Updated Subject',
            'topic': 'Updated Topic',
            'description': 'Updated Description',
            'due_date': '2024-01-01T12:00:00',
            'group': 'Updated_Group'
        }

        response = self.client.post(reverse('edit_task_form', args=[self.task.id]), updated_data)
        self.assertEqual(response.status_code, 200)
