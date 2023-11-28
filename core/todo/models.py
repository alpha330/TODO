from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class TaskTodo(models.Model):
    """_summary_
    models.py in task app to determine values of task and build database values
    type and relations
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = "user"
