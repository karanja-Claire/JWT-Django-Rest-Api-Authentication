from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser, BaseUserManager,PermissionsMixin
import uuid


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, first_name,last_name, email,password=None):
        if first_name is None:
            raise TypeError('Users should have a firstname')
        if last_name is None:
            raise TypeError('Users should have a lastname')
        if email is None:
            raise TypeError('Users should have a email')
        user = self.model(username=username, first_name = first_name ,last_name = last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,username,first_name,last_name, email, password=None):
        if first_name is None:
            raise TypeError('Users should have a firstname')
        if last_name is None:
            raise TypeError('Users should have a lastname')
        if password is None:
            raise TypeError('Users should have a password')
        if email is None:
            raise TypeError('Users should have a email')
        
        user = self.create_user(username, first_name,last_name, email)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
 


class User(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    email = models.CharField(max_length=256, unique=True, blank=False)
    username = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = UserManager()
