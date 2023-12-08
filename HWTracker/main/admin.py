from django.contrib import admin
from .models import Task, Group, GroupAdmin

admin.site.register(Task)
admin.site.register(Group, GroupAdmin)
