from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.hashers import get_random_string
from functools import wraps


def get_random_string32():
    return get_random_string(32)


def authorized_only(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        is_authenticated = request.user.is_authenticated
        if not is_authenticated:
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
        try:
            label = form.fields.get(field_name).label
        except AttributeError:
            label = 'Прочее' if field_name == '__all__' else field_name
        if label not in out:
            out[label] = []
        out[label] += [error.messages[0] for error in errors]
    return out
