from django.shortcuts import render, redirect
import requests
from urllib.parse import urlparse, parse_qs
import jwt
from .models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden


def index(request):
    template_name = 'main/index.html'
    username = request.session.get('username')
    if username is None:
        return render(request, template_name)
    return redirect('student')


def student(request):
    template_name = 'main/student.html'
    username = request.session.get('username')
    first_name, last_name = request.user.first_name, request.user.last_name
    is_admin = request.user.is_superuser
    if username is None:
        return redirect('/')
    tasks = get_tasks()
    return render(request, template_name,
                  {'first_name': first_name, 'last_name': last_name,
                   'tasks': tasks, 'is_admin': is_admin})


def add_task_form(request):
    template_name = 'main/add_task_form.html'
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = Task(subject=form.cleaned_data["subject"],
                            topic=form.cleaned_data["topic"],
                            description=form.cleaned_data["description"],
                            due_date=form.cleaned_data["due_date"])
            new_task.save()
            return redirect("/student")
    else:
        form = TaskForm()

    return render(request, template_name, {"form": form})


def handle_auth(request):
    code = parse_qs(urlparse(request.get_full_path()).query)['code'][0]
    data = get_user_information(code)
    decoded = jwt.decode(data['id_token'], '', algorithms='none', options={'verify_signature': False})
    email = decoded['email']
    name = email.split("@")[0]
    request.session['username'], request.session['email'] = name, email
    for key, value in decoded.items():
        print('{} => {}'.format(key, value))
    user, created = User.objects.get_or_create(username=name,
                                               email=email,
                                               first_name=decoded['given_name'],
                                               last_name=decoded['family_name'])
    if created:
        print("Пользователь создан")
    else:
        print("Пользователь уже есть")
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('student')


def logout(request):
    request.session.flush()
    return redirect('/')


def get_user_information(code):
    request = requests.post('https://oauth2.googleapis.com/token',
                            data={
                                'code': code,
                                'client_id': '437781818230-4tdb2qsrg7qhlmu5ud8dbge55mf8e79k.apps.googleusercontent.com',
                                'client_secret': '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',
                                'redirect_uri': 'http://127.0.0.1:8000/auth',
                                'grant_type': 'authorization_code',
                            })
    return request.json()


def get_tasks():
    return Task.objects.all()
