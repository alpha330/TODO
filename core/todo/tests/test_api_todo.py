import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import Users
from todo.models import TaskTodo

@pytest.fixture
def api_client():
    client = APIClient()
    return client
@pytest.fixture
def real_user():
    user = Users.objects.create_user(
        email="maral@maral.com",
        password="123qwe!@#",
        is_verified=True,
        )
    return user
    

@pytest.mark.django_db
class TestTodoApi:
    
    def test_get_todo_response_401_status(self,api_client):
        url = reverse("todo:api_v1:task-list")
        response = api_client.get(url)
        assert response.status_code == 401
        
    def test_create_task_response_401_status(self,api_client):
        url = reverse("todo:api_v1:task-list")
        data = {
            "title": "Test Task",
            "description":"This is a description for the task",
            "createdOn":datetime.now(),
        }
        response = api_client.post(url,data)
        assert response.status_code == 401
        
    def test_get_todo_response_200_status(self,api_client,real_user):
        url = reverse("todo:api_v1:task-list")
        api_client.force_login(user=real_user)
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_create_task_response_201_status(self,api_client,real_user):
        url = reverse("todo:api_v1:task-list")
        api_client.force_login(user=real_user)
        data = {
            "user":real_user,
            "title": "Test Task",
            "description":"This is a description for the task",
            "createdOn":datetime.now(),
        }
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_create_task_invalid_data_response_400_status(self,api_client,real_user):
        url = reverse("todo:api_v1:task-list")
        api_client.force_login(user=real_user)
        data = {
            "createdOn":datetime.now(),
        }
        response = api_client.post(url,data)
        assert response.status_code == 400
        
    def test_update_task_put_response_200_status(self,api_client,real_user):
        api_client.force_login(user=real_user)
        task = TaskTodo.objects.create(
            createdOn=datetime.now(),
            title="Task Title",
            complete=True,
            user=real_user,    
        )
        url = reverse("todo:api_v1:task-detail",kwargs={"pk":task.pk})
        data = {
            "title":"test-update",
            "complete":False,
        }
        response = api_client.put(url,data)
        assert response.status_code == 200
        
    def test_delete_task_delete_response_204_status(self,api_client,real_user):
        api_client.force_login(user=real_user)
        task = TaskTodo.objects.create(
            createdOn=datetime.now(),
            title="Task Title",
            complete=True,
            user=real_user,    
        )
        url = reverse("todo:api_v1:task-detail",kwargs={"pk":task.pk})
        response = api_client.delete(url)
        assert response.status_code == 204
        
        
    