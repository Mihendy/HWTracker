# main/urls.py
from django.urls import path
from django.views.generic import RedirectView


from . import views

urlpatterns = [
    path('student', views.student, name='student'),
    path('student/', RedirectView.as_view(url='/student')),
    path('logout', views.logout, name='logout'),
    path('logout/', RedirectView.as_view(url='/logout')),
    path('', views.index, name='index'),
    path('groups', views.groups, name='groups'),
    path('groups/', RedirectView.as_view(url='/groups')),
    path('groups/<int:group_id>', views.group_detail, name='group_detail'),
    # path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('taskform', views.add_task_form, name='taskform'),
    path('taskform/', RedirectView.as_view(url='/taskform')),
    path('taskform/<int:task_id>', views.add_task_form, name='edit_task_form'),
    # path('taskform/<int:task_id>/', views.add_task_form, name='edit_task_form'),
    path('checktask/', views.check_task, name='checktask'),
    path('deletetask/', views.delete_task, name='deletetask'),
    path('deletegroup/', views.delete_group, name='deletegroup'),
    path('invites/<str:_hash>', views.invites, name='invites'),
    path('deleteuser/', views.delete_user, name='deleteuser'),
]
