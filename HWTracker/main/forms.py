from datetime import datetime

from django import forms
from django.core.validators import validate_slug

from .models import Group, Task


def get_choices():
    return [(group.id, group.name) for group in Group.objects.all()] + [('other', 'Другая группа...')]


class TaskForm(forms.Form):
    group = forms.ChoiceField(
        label='Группа',
        choices=get_choices,
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'showOtherField(this)', 'id': 'groupInput'})
    )

    other_group = forms.CharField(
        label='Другая группа',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'otherGroupInput',
                   'placeholder': 'Название'}
        ),
        max_length=45,
        required=False,
        validators=[validate_slug],
        error_messages={'invalid': 'Это поле может содержать только буквы, цифры, знаки подчеркивания и дефис'}
    )

    subject = forms.CharField(
        label='Предмет',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        max_length=45
    )

    topic = forms.CharField(
        label='Тема',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
        max_length=45
    )

    description = forms.CharField(
        label='Описание',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, "id": "TextArea", "style": "resize: none;"}),
        max_length=130
    )

    due_date = forms.DateTimeField(
        widget=forms.TextInput(
            attrs={'type': 'datetime-local', 'class': 'form-control', 'max': datetime(2999, 12, 31)}
        ),
        label='Сдать до')

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']
