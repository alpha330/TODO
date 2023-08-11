from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TaskTodo
from django.urls import reverse_lazy
# Create your views here.
class TasksTodo(LoginRequiredMixin, ListView):
    model = TaskTodo
    context_object_name = "tasks"
    template_name = "todo/tasks.html"
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class CreateTasks(LoginRequiredMixin, CreateView):
    model = TaskTodo
    template_name = "todo/create-tasks.html"
    fields = '__all__'
    success_url = reverse_lazy("/tasks_todo")

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(CreateTasks, self).form_valid(form)

# class UpdateTask():
#     pass
# class CompleteTask():
#     pass
# class DeleteTask():
#     pass