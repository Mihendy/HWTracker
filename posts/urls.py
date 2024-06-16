from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('posts', views.post_list, name='posts'),
    path('posts/', RedirectView.as_view(url='/posts')),
    path('posts/<slug:post_slug>', views.post_detail, name='post'),
    path('deletepost/', views.delete_post, name='deletepost'),
]
