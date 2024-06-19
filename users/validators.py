import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User

MIN_LENGTH = 6


def validate_unique_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(_('Пользователь с таким email уже существует.'), code='invalid')


def validate_password_chars(value):
    if not re.match(r'^[\w.@+!#$%^&*;:?А-Яа-яA-Za-z0-9]*$', value):
        raise ValidationError(
            'Пароль может содержать только буквы, цифры и специальные символы из списка .@+!#$%^&*;:?',
            code='invalid_password'
        )


def validate_password_length(value):
    if len(value) < MIN_LENGTH:
        raise ValidationError(f'Пароль должен содержать не менее {MIN_LENGTH} символов.')
