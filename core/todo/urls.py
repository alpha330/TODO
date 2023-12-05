from django.urls import path, include
from todo import views

# determine urls form todo apps activity
app_name = "todo"

urlpatterns = [
    path("", views.TasksTodo.as_view(), name="tasks_todo"),
    path("create/", views.CreateTasks.as_view(), name="create_task"),
    path("update/<int:pk>", views.UpdateTask.as_view(), name="task_update"),
    path("complete/<int:pk>", views.CompleteTask.as_view(), name="task_complete"),
    path("delete/<int:pk>", views.DeleteTask.as_view(), name="delete_task"),
    path("api/v1/", include("todo.api.v1.urls")),
]
