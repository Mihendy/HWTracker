import json
import logging
from datetime import date
from urllib.parse import parse_qs, urlparse

import jwt
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from config import CLIENT_ID, CLIENT_SECRET, SERVER_DOMAIN
from users.forms import UserLoginForm, UserRegisterForm
from users.models import User

from .forms import GroupForm, TaskForm
from .functions import (authorized_only, editor_only, errors_to_text,
                        get_random_string32)
from .models import Group, Task

REDIRECT_URI = f'https://{SERVER_DOMAIN}/auth'
# REDIRECT_URI = f'http://{SERVER_DOMAIN}/auth'

logger = logging.getLogger(__name__)


def index(request):
    user = request.user
    template_name = 'main/index.html'
    reg_form_data = request.session.pop('invalid_reg_form', None)
    login_form_data = request.session.pop('invalid_login_form', None)
    reg_form = UserRegisterForm(initial=reg_form_data) if reg_form_data else UserRegisterForm(request.POST or None)
    login_form = UserLoginForm(initial=login_form_data) if login_form_data else UserLoginForm(request.POST or None)
    next_uri = request.GET.get('next') or request.session.get('next_uri')
    context = {'client_id': CLIENT_ID, 'redirect_uri': REDIRECT_URI,
               'reg_form': reg_form, 'login_form': login_form, 'register_state': False}
    reg_form_error_out = request.session.pop('invalid_reg_form_out', None)
    login_form_error_out = request.session.pop('invalid_login_form_out', None)
    if reg_form_error_out:
        context['form_errors'] = reg_form_error_out
        context['register_state'] = True
    elif login_form_error_out:
        context['form_errors'] = login_form_error_out
        context['register_state'] = False
    if user.is_authenticated:
        return redirect(next_uri or 'student')
    else:
        if next_uri:
            request.session['next_uri'] = next_uri
        return render(request, template_name, context)


@require_POST
def post_register(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['second_name']
        password = form.cleaned_data['password']
        user = User.objects.create(username=email,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name)
        user.set_password(password)
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        logger.info(f"User {user} registered and authorized")

        return redirect(request.session.get('next_uri') or 'student')
    else:
        out = errors_to_text(form)
        request.session['invalid_reg_form'] = form.data
        request.session['invalid_reg_form_out'] = out
        return redirect(reverse_lazy('index'))


@require_POST
def post_login(request):
    form = UserLoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        logger.info(f"User {user} authorized")

        return redirect(request.session.get('next_uri') or 'student')
    else:
        out = errors_to_text(form)
        request.session['invalid_login_form'] = form.data
        request.session['invalid_login_form_out'] = out
        return redirect(reverse_lazy('index'))


@require_POST
@authorized_only
@editor_only
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


@require_POST
@authorized_only
@editor_only
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


@require_POST
@authorized_only
@editor_only
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
        if task:
            related_posts_ids = list(map(lambda post: post.id, task.posts.all()))
            initial = {'posts': related_posts_ids}
            form = TaskForm(request.POST or None, instance=task, initial=initial)
        else:
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
                task = form.save(commit=False)
                task.save()
                task.group = group
                task.posts.set(form.cleaned_data["posts"])
                task.save()
                # task.subject = form.cleaned_data["subject"]
                # task.topic = form.cleaned_data["topic"]
                # task.description = form.cleaned_data["description"]
                # task.due_date = form.cleaned_data["due_date"]
                # task.group = group
                # print(form.cleaned_data["posts"])
                #
                # print(task.posts)
            else:
                task = form.save(commit=False)
                task.save()
                task.group = group
                task.posts.set(form.cleaned_data["posts"])
                task.save()

                # new_task = Task(
                #     subject=form.cleaned_data["subject"],
                #     topic=form.cleaned_data["topic"],
                #     description=form.cleaned_data["description"],
                #     due_date=form.cleaned_data["due_date"],ё
                #     group=group,
                # )
                # new_task.posts.set(form.cleaned_data["posts"])
                # new_task.save()

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
    try:
        code = parse_qs(urlparse(request.get_full_path()).query)['code'][0]
    except KeyError:
        logger.warning("User unauthorized")
        return HttpResponse(status=401)
    # todo: fix error
    try:
        data = get_user_information(code)
        decoded = jwt.decode(data['id_token'], '', algorithms='none', options={'verify_signature': False})
        email = decoded['email']
        first_name = decoded['given_name']
        last_name = decoded.get('family_name') or ""
        request.session['username'], request.session['email'] = email, email
        user, _ = User.objects.get_or_create(username=email,
                                             email=email,
                                             first_name=first_name,
                                             last_name=last_name)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        logger.info(f"User {user} authorized (google)")

        return redirect(request.session.get('next_uri') or 'student')
    except Exception:
        logger.error("Google User already registered as model")
        return HttpResponse(status=401)


def logout(request):
    request.session.flush()
    return redirect('/')


# not views

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


def get_task_separated_by_date(tasks: list[Task]) -> dict[date, list[Task]]:
    out = dict()
    for task in tasks:
        _date = task.due_date.date()
        if _date not in out:
            out[_date] = []
        out[_date].append(task)
    return out


def get_tasks(group: Group) -> list[Task]:
    return list(group.tasks.all()) if group else []


def get_groups() -> list[Group]:
    return list(Group.objects.all())
