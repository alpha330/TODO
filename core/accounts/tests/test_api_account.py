import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import Users
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    client = APIClient()
    return client
@pytest.fixture
def real_user():
    user = Users.objects.create_user(
        email="test@test.com",
        password="123qwe!@#",
        is_verified=True,
        )
    return user

@pytest.fixture
def real_user_unverified():
    user = Users.objects.create_user(
        email="maral@maral.com",
        password="123qwe!@#",
        is_verified=False,
        )
    return user

@pytest.mark.django_db
class TestApiAuthentications:
    
    def test_api_user_registration_response_201_status(self,api_client):
        data={
            "email":"test@test.com", 
            "password":"123qwe!@#", 
            "password_1":"123qwe!@#" 
            } 
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_api_user_registration_response_400_status(self,api_client):
        data={
            "email":"test", 
            "password":"123qwe!@#", 
            "password_1":"123qwe!@#" 
            } 
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data)
        assert response.status_code == 400
        
    def test_api_user_activation_response_405_status(self,api_client,real_user):
        refresh = RefreshToken.for_user(real_user)
        token = str(refresh.access_token)
        url = reverse("accounts:api-v1:activation",kwargs={"token":token})
        response = api_client.post(url)
        assert response.status_code == 405
        
    def test_api_user_activation_response_201_status(self,api_client,real_user_unverified):
        refresh = RefreshToken.for_user(real_user_unverified)
        token = str(refresh.access_token)
        url = reverse("accounts:api-v1:activation",kwargs={"token":token})
        data = {
            "uid":real_user_unverified.id,
            "token":token,
        }
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    
    