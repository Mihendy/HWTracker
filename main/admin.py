from django.contrib import admin

from .models import Group, GroupAdmin, Task

admin.site.register(Task)
admin.site.register(Group, GroupAdmin)
