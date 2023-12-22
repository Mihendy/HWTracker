# main/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('logout', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('groups', views.groups, name='groups'),
    path('groups/<str:name>', views.group_detail, name='group_detail'),
    path('taskform', views.add_task_form, name='taskform'),
    path('taskform/<int:task_id>', views.add_task_form, name='edit_task_form'),
    path('checktask/', views.check_task, name='checktask'),
    path('deletetask/', views.delete_task, name='deletetask'),
    path('deletegroup/', views.delete_group, name='deletegroup'),
]