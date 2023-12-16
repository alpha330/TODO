from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
from accounts.models import Users
from todo.models import TaskTodo


class Command(BaseCommand):
    help = "Inserting Dummy Data to Data-Base"

    def __init__(self):
        self.faker = Faker()

    def handle(self, *args, **options):
        user = Users.objects.create_user(email=self.faker.email(), password="123qwe!@#")

        for _ in range(5):
            TaskTodo.objects.create(
                user=user,
                title=self.faker.paragraph(nb_sentences=3),
                complete=False,
                createdOn=datetime.now(),
            )
