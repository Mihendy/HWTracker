from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from social_django.utils import psa

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return HttpResponse("Login page")


@psa('social:complete')
def complete(request, backend, *args, **kwargs):
    """View to handle the completion of the social authentication."""
    # This view is decorated with @psa, which stands for Python Social Auth.
    # It handles the social authentication process.
    print('nigger')
    # Your code to process the authenticated user goes here.
    # For example, you can get user information from kwargs['response'].

    return redirect('/')  # Redirect the user to the home page after authentication.