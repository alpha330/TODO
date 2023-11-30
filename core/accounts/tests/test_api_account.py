import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime
from accounts.models import Users
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

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
def fake_token():
    user = Users.objects.create_user(
        email="ali@test.com",
        password="123qwe!@#",
        is_verified=True,
        )
    user_obj = get_object_or_404(Users,email=user.email)
    ref_token = RefreshToken.for_user(user_obj)
    token = str(ref_token.access_token)
    return token

@pytest.fixture
def real_user_unverified():
    user = Users.objects.create_user(
        id = 1 ,
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
        
    def test_api_user_registration_response_201_status(self,api_client):
        data={
            "email":"test@test.com", 
            "password":"123qwe!@#", 
            "password_1":"123qwe!@#" 
            } 
        url = reverse("accounts:api-v1:registration")
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_api_user_confirm_get_response_200_status(self,api_client,real_user_unverified):
        api_client.force_login(real_user_unverified)
        user = get_object_or_404(Users, email=real_user_unverified.email)
        ref_tok = RefreshToken.for_user(user)
        token = str(ref_tok.access_token)
        url = reverse("accounts:api-v1:activation",kwargs={"token":token})
        response = api_client.get(url)
        assert response.status_code == 200
        
    def test_api_user_reconfirm_post_201_status(self,api_client,real_user_unverified):
        api_client.force_login(real_user_unverified)
        user_obj = get_object_or_404(Users,email=real_user_unverified.email)
        url = reverse("accounts:api-v1:reconfirmation")
        data = {"email":user_obj.email}
        response = api_client.post(url,data)
        assert response.status_code == 201
        
    def test_api_user_reconfirm_post_400_status(self,api_client,real_user):
        api_client.force_login(real_user)
        user_obj = get_object_or_404(Users,email=real_user.email)
        url = reverse("accounts:api-v1:reconfirmation")
        data = {"email":user_obj.email}
        response = api_client.post(url,data)
        assert response.status_code == 400
        
    def test_api_user_change_password_put_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password":"123qwe!@#",
            "new_password_1":"123qwe!@#123",
            "new_password_2":"123qwe!@#123",
        }
        response = api_client.put(url,data)
        assert response.status_code == 200
        
    def test_api_user_change_password_put_400_status(self,api_client,real_user):
        api_client.force_login(real_user)
        url = reverse("accounts:api-v1:change-password")
        data = {
            "old_password":"123qwe!@#",
            "new_password_1":"123qwe",
            "new_password_2":"123qwe!@#123",
        }
        response = api_client.put(url,data)
        assert response.status_code == 400
        
    def test_api_v1_user_create_jwt_token_post_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        url = reverse("accounts:api-v1:create-jwt-token")
        data = {
            "email":real_user.email,
            "password":"123qwe!@#",
        }
        response = api_client.post(url,data)
        assert response.status_code == 200
        
    def test_api_v1_user_refresh_jwt_token_post_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        user = get_object_or_404(Users ,email=real_user.email)
        tok_ref = str(RefreshToken.for_user(user))
        url = reverse("accounts:api-v1:refresh-jwt-token")
        data = {
            "refresh":tok_ref,
        }
        response = api_client.post(url,data)
        assert response.status_code == 200
        
    def test_api_v1_user_verify_jwt_token_post_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        user = get_object_or_404(Users ,email=real_user.email)
        tok_ref = RefreshToken.for_user(user)
        token_access = str(tok_ref.access_token)
        url = reverse("accounts:api-v1:verify-jwt-token")
        data = {
            "token":token_access,
        }
        response = api_client.post(url,data)
        assert response.status_code == 200
        
    def test_api_v1_user_reset_password_put_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        user = get_object_or_404(Users ,email=real_user.email)
        tok_ref = RefreshToken.for_user(user)
        token_access = str(tok_ref.access_token)
        url = reverse("accounts:api-v1:reset-password",kwargs={"token":token_access})
        data = {
            "new_password":"123/$$#!@/qwe",
            "new_password_1":"123/$$#!@/qwe",
        }
        response = api_client.put(url,data)
        assert response.status_code == 200
        
    def test_api_v1_user_reset_password_link_post_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        url = reverse("accounts:api-v1:send-reset-password-link")
        data = {
            "email":real_user.email,
        }
        response = api_client.post(url,data)
        assert response.status_code == 200
        
    def test_api_v1_costume_auth_token_post_200_status(self,api_client,real_user):
        api_client.force_login(real_user)
        url = reverse("accounts:api-v1:token-login")
        data = {
            "email":real_user.email,
            "password":"123qwe!@#",
        }
        response = api_client.post(url,data)
        assert response.status_code == 200
        
    def test_api_v1_user_logout_token_post_204_status(self,api_client,real_user):
        api_client.force_authenticate(real_user)
        user = get_object_or_404(Users ,email=real_user.email)
        Token.objects.create(user=user)
        url = reverse("accounts:api-v1:token-logout")
        response = api_client.post(url)
        assert response.status_code == 204
    
    