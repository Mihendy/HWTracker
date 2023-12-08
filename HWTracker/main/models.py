from django.db import models
from django.contrib import admin


class Task(models.Model):
    subject = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    description = models.TextField(max_length=150)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subject} - {self.topic}'

    def get_absolute_url(self):
        return f"/task/{self.id}/"

    class Meta:
        ordering = ['due_date']


class Group(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        pass


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_user_count')

    def get_user_count(self, obj):
        return obj.users.count()

    get_user_count.short_description = 'Количество пользователей'
