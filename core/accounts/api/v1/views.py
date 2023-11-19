from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistrationSerializer,CustomAuthTokenSerializer,CustomTokenObtainPairSerializer
    ,ChangePasswordSerializer
    )
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

Users=get_user_model()
class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "email":serializer.validated_data["email"]
            }
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CustomAuthToken(ObtainAuthToken):
    serializer_class=CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
        
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ChangePasswordApiView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    Model = Users
    permission_classes = [IsAuthenticated]
    
    def get_object(self,queryset=None):
        obj = self.request.user
        return obj
    def put(self,request,*args,**kwargs):
        self.object=self.get_object()
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            #Check Old Password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old password":"Is Wrong"},status=status.HTTP_400_BAD_REQUEST)
            #set new password and updates password and save
            self.object.set_password(serializer.data.get('new_password_1'))
            self.object.save()
            return Response({"detail":"password has been update"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class TestEmailApiView(generics.GenericAPIView):
    
    def get(self,request,*args,**kwargs):
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
            )
        return Response("email sent")
    