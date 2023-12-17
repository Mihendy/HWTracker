# HWTracker/urls.py
from django.contrib import admin
from django.urls import include, path

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth', views.handle_auth),
]