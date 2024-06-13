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
            return HttpResponseRedirect(f'/?next={request.get_full_path()}')
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


def errors_to_text(form):
    out = {}
    errs = form.errors.as_data()
    for field_name, errors in errs.items():
        label = form.fields[field_name].label or field_name
        if label not in out:
            out[label] = []
        out[label] += [error.messages[0] for error in errors]
    return out
