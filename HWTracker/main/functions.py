from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.hashers import get_random_string
from functools import wraps


def get_random_string32():
    return get_random_string(32)


def authorized_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        username = request.session.get('username')
        if username is None:
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)

    return wrapper


def editor_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        is_editor = request.user.is_editor
        if not is_editor:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return wrapper
