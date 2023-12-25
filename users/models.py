from django.contrib.auth.models import AbstractUser
from django.db import models

# noinspection PyUnresolvedReferences
from main.models import Group


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=False)
    email = models.EmailField(blank=False, null=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    is_editor = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('email',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'