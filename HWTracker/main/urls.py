# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('social-auth/complete/google-oauth2/', views.test, name='google-auth-complete'),
    path('', views.index, name='index'),
]