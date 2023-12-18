import json
from urllib.parse import parse_qs, urlparse

import jwt
import requests
from django.contrib.auth import login
from django.db.models import ProtectedError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render

# noinspection PyUnresolvedReferences
from users.models import User

from .forms import TaskForm
from .models import Group, Task

CLIENT_ID = '437781818230-4tdb2qsrg7qhlmu5ud8dbge55mf8e79k.apps.googleusercontent.com'

REDIRECT_URI = 'http://127.0.0.1:8000/auth'

CLIENT_SECRET = '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'


def index(request):
    template_name = 'main/index.html'
    username = request.session.get('username')
    if username is None:
        return render(request, template_name, {'client_id': CLIENT_ID,
                                               'redirect_uri': REDIRECT_URI})
    return redirect('student')


def check_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('task_id')
        user_id = data.get('user_id')
        status = data.get('status')
        # print(task_id, user_id, status)
        if task_id is None or user_id is None or status is None:
            return JsonResponse({'success': False})
        task = Task.objects.get(id=task_id)
        user = User.objects.get(id=user_id)

        try:
            if status == 'incompleted':
                # print(f"adding {user} to {task}")
                task.status = 'completed'
                task.completed_by.add(user)

            else:
                # print(f"removing {user} from {task}")
                task.status = 'incompleted'
                task.completed_by.remove(user)
            task.save()
        except Task.DoesNotExist:
            print(f'task {task} does not exist')
        except User.DoesNotExist:
            print(f'user {user} does not exist')

        return JsonResponse({'success': True})


def student(request):
    template_name = 'main/student.html'
    username = request.session.get('username')

    if username is None:
        return redirect('/')

    user = request.user
    first_name = user.first_name
    last_name = user.last_name
    group = user.group
    is_editor = request.user.is_editor

    if is_editor:
        tasks = Task.objects.all()
    else:
        tasks = get_tasks(user.group)
    data = get_task_separated_by_date(tasks)
    for task in tasks:
        task.status = 'completed' if task.is_completed_by_user(user) else 'incompleted'

    return render(request, template_name,
                  {'first_name': first_name, 'last_name': last_name, 'user': request.user,
                   'data': data, 'is_editor': is_editor, 'group': group.name if group is not None else 'Нет группы'})


def add_task_form(request):
    template_name = 'main/add_task_form.html'
    username = request.session.get('username')
    if username is None:
        return redirect('/')
    if not request.user.is_editor:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            _id = form.cleaned_data["group"]
            if _id == 'other':
                new_group = Group(name=form.cleaned_data["other_group"])
                new_group.save()
                _id = new_group.pk
            group = Group.objects.get(id=_id)
            new_task = Task(subject=form.cleaned_data["subject"],
                            topic=form.cleaned_data["topic"],
                            description=form.cleaned_data["description"],
                            due_date=form.cleaned_data["due_date"], group=group)
            new_task.save()
            return redirect("/student")
        else:
            out = {}
            errs = form.errors.as_data()
            for field_name, errors in errs.items():
                label = form.fields[field_name].label or field_name
                if label not in out:
                    out[label] = []
                out[label] += [error.messages[0] for error in errors]

            return render(request, template_name, {"form": form, "form_errors": out})
    else:
        form = TaskForm()

    return render(request, template_name, {"form": form})


def handle_auth(request):
    code = parse_qs(urlparse(request.get_full_path()).query)['code'][0]
    data = get_user_information(code)
    decoded = jwt.decode(data['id_token'], '', algorithms='none', options={'verify_signature': False})
    email = decoded['email']
    first_name = decoded['given_name']
    last_name = decoded.get('family_name') or ""
    name = email.split("@")[0]
    request.session['username'], request.session['email'] = name, email
    user, _ = User.objects.get_or_create(username=name,
                                         email=email,
                                         first_name=first_name,
                                         last_name=last_name)
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('student')


def logout(request):
    request.session.flush()
    return redirect('/')


def get_task_separated_by_date(tasks: list[Task]) -> dict[str, list[Task]]:
    out = dict()
    for task in tasks:
        date = task.due_date.date()
        if date not in out:
            out[date] = []
        out[date].append(task)
    return out


def get_user_information(code):
    request = requests.post('https://oauth2.googleapis.com/token',
                            data={
                                'code': code,
                                'client_id': CLIENT_ID,
                                'client_secret': CLIENT_SECRET,
                                'redirect_uri': REDIRECT_URI,
                                'grant_type': 'authorization_code',
                            })
    return request.json()


def get_tasks(group: Group) -> list[Task]:
    return list(group.tasks.all()) if group else []


def get_groups() -> list[Group]:
    return list(Group.objects.all())
