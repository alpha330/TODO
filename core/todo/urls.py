from django.urls import path
from .views import TasksTodo,CreateTasks

app_name = 'todo'

urlpatterns =[
    path("", TasksTodo.as_view(),name="tasks_todo"),
    path("create/", CreateTasks.as_view(),name="create_task"),
#     path("update/<int:pk>", UpdateTask.as_view(),name="task_update"),
#     path("complete/<int:pk>", CompleteTask.as_view(),name="task_complete"),
#     path("delete/<int:pk>", DeleteTask.as_view(),name="delete_task"),
]