from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import index, student, logout, group_detail, add_task_form, check_task, delete_task

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_student_url_is_resolved(self):
        url = reverse('student')
        self.assertEquals(resolve(url).func, student)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)

    def test_group_detail_url_is_resolved(self):
        url = reverse('group_detail', args=['example_group'])
        self.assertEquals(resolve(url).func, group_detail)

    def test_taskform_url_is_resolved(self):
        url = reverse('taskform')
        self.assertEquals(resolve(url).func, add_task_form)

    def test_check_task_url_is_resolved(self):
        url = reverse('checktask')
        self.assertEquals(resolve(url).func, check_task)

    def test_delete_task_url_is_resolved(self):
        url = reverse('deletetask')
        self.assertEquals(resolve(url).func, delete_task)
