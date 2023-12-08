from datetime import datetime
from django.db import connection
from django import forms

from .models import Task, Group


def get_choices():
    return [(group.id, group.name) for group in Group.objects.all()]


class TaskForm(forms.Form):
    group = forms.ChoiceField(label='Группа', choices=get_choices)
    subject = forms.CharField(label='Предмет', widget=forms.TextInput(attrs={'class': 'field-of-subject'}))
    topic = forms.CharField(label='Тип', widget=forms.TextInput(attrs={'class': 'field-of-topic'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'field-of-description'}))
    due_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'field-of-due_date'}),
        label='Сдать до',)
    
   

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']