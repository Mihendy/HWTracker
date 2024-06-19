from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from .models import User
from .validators import (validate_password_chars, validate_password_length,
                         validate_unique_email)


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Имя'}),
        max_length=150
    )

    second_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Фамилия'}),
        max_length=150
    )

    email = forms.EmailField(
        label='Эл. почта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Эл. почта'}),
        validators=[validate_unique_email],
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Пароль'}),
        max_length=128,
        validators=[validate_password_length, validate_password_chars]
    )

    password_re = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Повтор пароля'}),
        max_length=128
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_re = cleaned_data.get("password_re")

        need_to_check = password is not None and password_re is not None

        if password != password_re and need_to_check:
            raise ValidationError("Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = User
        fields = ['email', 'first_name', 'second_name']


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label='Эл. почта',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Эл. почта'}),
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Пароль'}),
        max_length=128
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        try:
            user = User.objects.get(username=email)
            user.check_password(password)
            if not user.check_password(password):
                raise ValidationError("Неверный email или пароль.")
        except User.DoesNotExist:
            raise ValidationError("Неверный email или пароль.")

        return cleaned_data

    class Meta:
        model = User
        fields = ['email']

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     if kwargs.get('instance'):
    #         self.fields['group'].initial = kwargs['instance'].group_id
