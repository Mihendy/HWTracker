from django.test import SimpleTestCase
from django.urls import resolve, reverse

from main.views import (add_task_form, check_task, delete_group, delete_task,
                        delete_user, group_detail, index, invites, logout,
                        student)


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
        group_id = 1
        url = reverse('group_detail', args=[group_id])
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

    def test_delete_group_url_is_resolved(self):
        url = reverse('deletegroup')
        self.assertEquals(resolve(url).func, delete_group)

    def test_invites_url_is_resolved(self):
        _hash = 'example_hash'
        url = reverse('invites', args=[_hash])
        self.assertEquals(resolve(url).func, invites)

    def test_delete_user_url_is_resolved(self):
        url = reverse('deleteuser')
        self.assertEquals(resolve(url).func, delete_user)
