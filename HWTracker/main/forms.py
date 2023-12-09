from datetime import datetime
from django.db import connection
from django import forms

from .models import Task, Group


def get_choices():
    return [(group.id, group.name) for group in Group.objects.all()]


class TaskForm(forms.Form):
    group = forms.ChoiceField(label='Группа', choices=get_choices,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Предмет', widget=forms.TextInput(attrs={'class': 'form-control'}))
    topic = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, "id": "TextArea", "style": "resize: none;"}), max_length=150)
    due_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Сдать до', )

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']
