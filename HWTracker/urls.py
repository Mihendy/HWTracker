# HWTracker/urls.py
from django.contrib import admin
from django.urls import include, path
# noinspection PyUnresolvedReferences
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('posts.urls')),
    path('auth', views.handle_auth),
]
