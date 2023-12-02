# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('logout', views.logout, name='logout'),
    path('', views.index, name='index'),
]