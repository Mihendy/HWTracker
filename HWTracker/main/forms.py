from datetime import datetime

from django import forms

from .models import Task


class TaskForm(forms.Form):
    subject = forms.CharField(label='Предмет')
    topic = forms.CharField(max_length=32, label='Тип')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    due_date = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label='Сдать до')

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']
