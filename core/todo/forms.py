from django import forms
from .models import TaskTodo


class FormUpdateTask(forms.ModelForm):
    """
    Model form for updating a task todo object
    """

    title = forms.CharField(max_length=255)

    class Meta:
        model = TaskTodo
        fields = ("title",)
