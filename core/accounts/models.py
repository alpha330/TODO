from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError(_("Users must have an Email"))
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault("is_superuser",True)
        kwargs.setdefault("is_active",True)
        if kwargs.get('is_staff') is not True:
            raise ValueError(_("superuser must have staff permissions"))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have superuser permissions"))
        return self.create_superuser(email, password, **kwargs)
class Users(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email