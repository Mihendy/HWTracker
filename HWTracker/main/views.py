from django.shortcuts import render, redirect
import requests
from urllib.parse import urlparse, parse_qs
import jwt
from .models import Task


def index(request):
    template_name = 'main/index.html'
    username = request.session.get('username')
    if username is None:
        return render(request, template_name)
    return redirect('student')


def student(request):
    template_name = 'main/student.html'
    username = request.session.get('username')
    if username is None:
        return redirect('/')
    tasks = get_tasks()
    return render(request, template_name, {'username': username, 'tasks': tasks})


def handle_auth(request):
    code = parse_qs(urlparse(request.get_full_path()).query)['code'][0]
    data = get_user_information(code)
    decoded = jwt.decode(data['id_token'], '', algorithms='none', options={'verify_signature': False})
    request.session['username'] = decoded['name']
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
