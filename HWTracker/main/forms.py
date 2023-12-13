from datetime import datetime
from django.db import connection
from django import forms

from .models import Task, Group


def get_choices():
    return [(group.id, group.name) for group in Group.objects.all()]


class TaskForm(forms.Form):
    group = forms.ChoiceField(label='Группа', choices=get_choices,
                              widget=forms.Select(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Предмет', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=45)
    topic = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=45)
    description = forms.CharField(label='Описание', widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, "id": "TextArea", "style": "resize: none;"}), max_length=130)
    due_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type': 'datetime-local', 'class': 'form-control', 'max': datetime(2999, 12, 31)}),
        label='Сдать до')

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']
