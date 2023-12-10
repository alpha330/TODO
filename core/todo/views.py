from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TaskTodo
from .forms import FormUpdateTask
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect


# Create your views here.
class TasksTodoJob(LoginRequiredMixin, ListView):
    """
    Create View For Listing Tasks appends to template
    """

    model = TaskTodo
    context_object_name = "tasks"
    template_name = "todo/tasks.html"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CreateTasks(LoginRequiredMixin, CreateView):
    """
    Create View for Creating a new task and append it in the database
    """

    model = TaskTodo
    fields = ["title"]
    success_url = reverse_lazy("todo:tasks_todo")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super(CreateTasks, self).form_valid(form)
        return response


class UpdateTask(LoginRequiredMixin, UpdateView):
    """
    Update view of tasks
    """

    model = TaskTodo
    success_url = reverse_lazy("todo:tasks_todo")
    form_class = FormUpdateTask
    template_name = "todo/update-task.html"


class CompleteTask(LoginRequiredMixin, View):
    """
    Marks as complete when clicked on the button
    """

    model = TaskTodo
    success_url = reverse_lazy("todo:tasks_todo")

    def get(self, request, *args, **kwargs):
        object = TaskTodo.objects.get(id=kwargs.get("pk"))
        object.complete = True
        object.save()
        return redirect(self.success_url)


class DeleteTask(LoginRequiredMixin, DeleteView):
    """
    Deletes an existing task from the database
    """

    model = TaskTodo
    context_object_name = "task"
    success_url = reverse_lazy("tasks_todo")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

