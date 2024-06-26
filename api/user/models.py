import json
from datetime import datetime
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(max_length=255,null=True,default="",blank=True)
    
    class Meta:
        db_table='departments'

    def __str__(self) -> str:
        return self.name

class User(models.Model):
    permission_choices = (
        ("admin","Admin"),
        ("student","Student"),
        ("officer","Officer")
    )
    gender_choices = (
        ("male","Male"),
        ("female","Female")
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,unique=True)
    gender = models.CharField(max_length=100, choices=gender_choices, default="male")
    permission = models.CharField(max_length=100,choices=permission_choices,default="student")
    username = models.CharField( max_length=100,unique=True)
    password = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)
    avatar = models.CharField(max_length=255,default="default.jpg")
    department = models.OneToOneField(Department,null=True,blank=True,on_delete=models.SET_NULL, default=None)
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
        return self.name



