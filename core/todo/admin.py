from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskTodo
# Register your models here.

class TaskTodoAdmin(UserAdmin):
    model = TaskTodo
    list_display = ['title','user','createdOn','updateOn','complete']
    list_filter = ['user','complete']
    ordering = ('createdOn',)
    search_fields=('title','user',)


admin.site.register(TaskTodo)