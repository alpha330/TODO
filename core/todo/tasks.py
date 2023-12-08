from celery import shared_task
from time import sleep
from todo.models import TaskTodo

@shared_task
def delete_completed_tasks():
    sleep(10)
    completed_task = TaskTodo.objects.filter(complete=True)
    completed_task.delete()
    return print("completed task has been deleted")