import json
import logging
from datetime import date
from urllib.parse import parse_qs, urlparse

import jwt
import requests
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .functions import get_random_string32
from users.models import User

from .forms import TaskForm, GroupForm
from .models import Group, Task

from .functions import authorized_only, editor_only, errors_to_text
from config import SERVER_DOMAIN, CLIENT_SECRET, CLIENT_ID

REDIRECT_URI = f'http://{SERVER_DOMAIN}/auth'

logger = logging.getLogger(__name__)


def index(request):
    template_name = 'main/index.html'
    username = request.session.get('username')
    if username is None:
        return render(request, template_name, {'client_id': CLIENT_ID,
                                               'redirect_uri': REDIRECT_URI})
    return redirect('student')


def delete_task(request):
    data = json.loads(request.body)
    task_id = data.get('task_id')
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
    except Task.DoesNotExist:
        logger.warning(f"Task with id={task_id} does not exist")
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})


def delete_group(request):
    data = json.loads(request.body)
    group_id = data.get('group_id')
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
    except Group.DoesNotExist:
        logger.warning(f"Group with id={group_id} does not exist")
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})


def delete_user(request):
    data = json.loads(request.body)
    user_id = data.get('user_id')
    try:
        user = User.objects.get(id=user_id)
        user.group = None
        user.save()
    except User.DoesNotExist:
        logger.warning(f"User with id={user_id} does not exist")
        return JsonResponse({'success': False})

    return JsonResponse({'success': True})


def check_task(request):
    data = json.loads(request.body)
    task_id = data.get('task_id')
    user_id = data.get('user_id')
    status = data.get('status')
    if task_id is None or user_id is None or status is None:
        return JsonResponse({'success': False})
    try:
        task = Task.objects.get(id=task_id)
        user = User.objects.get(id=user_id)
        if status == 'incompleted':
            task.status = 'completed'
            task.completed_by.add(user)
        else:
            task.status = 'incompleted'
            task.completed_by.remove(user)
        task.save()
    except Task.DoesNotExist:
        logger.warning(f"Task with id={task_id} does not exist")
    except User.DoesNotExist:
        logger.warning(f"User with id={user_id} does not exist")
    return JsonResponse({'success': True})


@authorized_only
def student(request):
    template_name = 'main/student.html'

    user = request.user
    group = user.group
    is_editor = request.user.is_editor

    if is_editor:
        tasks = Task.objects.all()
    else:
        tasks = get_tasks(user.group)
    data = get_task_separated_by_date(tasks)
    for task in tasks:
        task.status = 'completed' if task.is_completed_by_user(user) else 'incompleted'

    return render(request, template_name, {
        'user': request.user,
        'data': data,
        'group': group.name if group is not None else 'Нет группы'
    })


@authorized_only
@editor_only
def add_task_form(request, task_id=None):
    template_name = 'main/add_task_form.html'

    if task_id:
        # Editing an existing task
        page_title = 'Изменение'
        task = get_object_or_404(Task, id=task_id)
        form = TaskForm(request.POST or None, instance=task)
    else:
        # Creating a new task
        page_title = 'Создание'
        form = TaskForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            _id = form.cleaned_data["group"]
            if _id == 'other':
                new_group = Group(name=form.cleaned_data["other_group"])
                new_group.save()
                _id = new_group.pk
            group = Group.objects.get(id=_id)

            if task_id:
                task.subject = form.cleaned_data["subject"]
                task.topic = form.cleaned_data["topic"]
                task.description = form.cleaned_data["description"]
                task.due_date = form.cleaned_data["due_date"]
                task.group = group
                task.save()
            else:
                new_task = Task(
                    subject=form.cleaned_data["subject"],
                    topic=form.cleaned_data["topic"],
                    description=form.cleaned_data["description"],
                    due_date=form.cleaned_data["due_date"],
                    group=group
                )
                new_task.save()

            return redirect("/student")
        else:
            out = errors_to_text(form)

            return render(request, template_name,
                          {'page': page_title, 'user': request.user, "form": form, "form_errors": out})

    return render(request, template_name, {'page': page_title, 'user': request.user, "form": form})


@authorized_only
@editor_only
def group_detail(request, group_id):
    template_name = 'main/group_detail.html'

    group = get_object_or_404(Group, id=group_id)
    form = GroupForm(request.POST or None, instance=group)
    if request.method == "POST":
        if 'rename' in request.POST:
            if form.is_valid():
                group.name = form.cleaned_data['name']
                group.save()
            else:
                out = errors_to_text(form)
                return render(request, template_name,
                              {'user': request.user, 'group': group, "form": form, "form_errors": out})
        elif 'update' in request.POST:
            group._hash = get_random_string32()
            group.save()
            return redirect(request.path)

    return render(request, template_name, {'user': request.user, 'group': group, "form": form})


@authorized_only
@editor_only
def groups(request):
    template_name = 'main/groups.html'
    all_groups = get_groups()
    form = GroupForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            new_group = Group(name=form.cleaned_data["name"])
            new_group.save()
            return redirect('/groups')
        else:
            out = errors_to_text(form)
            return render(
                request,
                template_name,
                {'groups': all_groups, 'user': request.user, 'form': form, "form_errors": out}
            )
    return render(request, template_name, {'groups': all_groups, 'user': request.user, 'form': form})


@authorized_only
def invites(request, _hash):
    group = get_object_or_404(Group, _hash=_hash)
    group.users.add(request.user)
    return redirect('student')


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
    logger.info(f"User {user} authorized")
    return redirect('student')


def logout(request):
    request.session.flush()
    return redirect('/')


def get_task_separated_by_date(tasks: list[Task]) -> dict[date, list[Task]]:
    out = dict()
    for task in tasks:
        _date = task.due_date.date()
        if _date not in out:
            out[_date] = []
        out[_date].append(task)
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
