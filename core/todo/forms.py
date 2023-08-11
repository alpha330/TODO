from django import forms
from .models import TaskTodo


class TaskCreateForm(forms.ModelForm):

    class Meta:
        model = TaskTodo
        fields = ['title']
