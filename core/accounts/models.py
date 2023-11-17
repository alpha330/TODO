from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class UserManager(BaseUserManager):
    """_summary_
    UserManager Class can manage topology of creation simple user
    and Super user with this class inherits From BaseUserManager
    can rules the workflow of Authentication
    """
    def create_user(self,email,password,**kwargs):
        """_summary_
        this def for creating user with data comes from clients with extra fields as kwargs
        :param email: str -> email address of client
        :param password: str -> password of client
        :return: instance of created user
        
        """
        if not email:
            raise ValueError(_("Users must have an Email"))
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**kwargs):
        """_summary_
        This method is used to create super users in our application
        :param email: str -> email address of client
        :param password: str -> password of client
        :return: instance of created super user
        
        """
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)
        kwargs.setdefault("is_active",True)
        if kwargs.get('is_staff') is not True:
            raise ValueError(_("superuser must have staff permissions"))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have superuser permissions"))
        return self.create_user(email, password, **kwargs)
    
class Users(AbstractBaseUser,PermissionsMixin):
    """_summary_
    Users model authentication app for customization auth model
    this model class inherent from AbstractBaseUser and PermissionMixin parent class
    to make it work with Django's built-in Authentication system
    USERNAME field change to email 
    and required fields can add in required fields 
    """
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.email