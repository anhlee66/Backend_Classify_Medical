from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table='departments'

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.BooleanField(default=True)
    permission = models.CharField(max_length=100,default='admin')
    # deparment = models.ForeignKey(Department,on_delete=models.CASCADE,default=0)
    username = models.CharField( max_length=100)
    password = models.CharField(max_length=255)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = "username,email,password"
    class Meta:
        db_table = "users"

    def authenticate(username,password):
        try:
            return User.objects.get(username=username,password=password)
        except:
            return None


    def __str__(self):
        return "{}".format(self.username)


class Log(models.Model):
    created = models.DateTimeField()
    tag = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        db_table = "logs"
