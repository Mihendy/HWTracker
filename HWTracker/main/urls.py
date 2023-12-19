# main/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('logout', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('group/<str:name>/', views.group_detail, name='group_detail'),
    path('taskform', views.add_task_form, name='taskform'),
    path('checktask/', views.check_task, name='checktask')
]