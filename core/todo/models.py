from django.db import models
from accounts.models import Users
# Create your models here.
class TaskTodo(models.Model):
    user = models.ForeignKey(
        Users, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    createdOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    class Meta():
        order_with_respect_to ="user"
 