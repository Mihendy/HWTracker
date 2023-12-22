from django.conf import settings
from django.contrib import admin
from django.db import models
from .functions import get_random_string32


class Group(models.Model):
    name = models.CharField(max_length=50)
    _hash = models.CharField(max_length=256, default=get_random_string32)

    def __str__(self):
        return self.name

    def get_members_count(self):
        return self.users.count()

    def get_tasks_count(self):
        return self.tasks.count()

    class Meta:
        ordering = ['name']


class Task(models.Model):
    subject = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    due_date = models.DateTimeField()
    completed_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='completed_tasks')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')

    def __str__(self):
        return f'{self.subject} - {self.topic}'

    def is_completed_by_user(self, user):
        return self.completed_by.filter(pk=user.pk).exists()
    
    def get_statistics(self) -> (int, int):
        return (self.completed_by.count(), self.group.users.count())

    class Meta:
        ordering = ['due_date']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count')

    def get_user_count(self, obj):
        return obj.users.count()

    get_user_count.short_description = 'Количество пользователей'
