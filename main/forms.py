from datetime import datetime

from django import forms

from posts.models import Post
from .models import Group, Task
from .validators import validate_extended_slug


def get_choices():
    return [(group.id, group.name) for group in Group.objects.all()] + [('other', 'Другая группа...')]


class TaskForm(forms.ModelForm):
    group = forms.ChoiceField(
        label='Группа',
        choices=get_choices,
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'showOtherField(this)', 'id': 'groupInput'}),
    )

    other_group = forms.CharField(
        label='Другая группа',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'id': 'otherGroupInput',
                   'placeholder': 'Название'}
        ),
        max_length=45,
        required=False,
        validators=[validate_extended_slug],
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

    posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Связанные статьи',
        required = False
    )

    class Meta:
        model = Task
        fields = ['subject', 'topic', 'description', 'due_date']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            self.fields['group'].initial = kwargs['instance'].group_id


class GroupForm(forms.ModelForm):
    name = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control form-control-lg', 'autocomplete': 'off', 'id': 'group-name',
                   'placeholder': 'Название группы'}),
        max_length=45,
        validators=[validate_extended_slug],
        error_messages={'invalid': 'Это поле может содержать только буквы, цифры, знаки подчеркивания и дефис'}
    )

    class Meta:
        model = Group
        fields = ['name']
