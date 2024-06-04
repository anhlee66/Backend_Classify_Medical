import json
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table='departments'

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    gender = models.BooleanField(default=True)
    permission = models.CharField(max_length=100,default='admin')
    username = models.CharField( max_length=100,unique=True)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = "username,email,password"
    # class Meta:
    #     db_table = "users"

    def authenticate(username,password):
        try:
            return User.objects.get(username=username,password=password)
        except:
            return None


    def __str__(self):
        user = {
            "name":self.name,
            "email":self.email,
            "gender":self.gender,
            "username":self.username,
            "password":self.password,
            "permission":self.permission
        }
        return json.dumps(user)



