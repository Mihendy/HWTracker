from django.db import models
from django.contrib import admin
from django.conf import settings


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

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

    class Meta:
        ordering = ['due_date']


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count')

    def get_user_count(self, obj):
        return obj.users.count()

    get_user_count.short_description = 'Количество пользователей'
