from django.db import models
from django import forms

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table='departments'

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.BooleanField()
    isAdmin = models.BooleanField()
    isStudent = models.BooleanField()
    isOfficer = models.BooleanField()
    deparment = models.ForeignKey(Department,on_delete=models.CASCADE)
    username = models.CharField( max_length=100)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = "users"

    def check_password(self,_password):
        if self.password == _password:
            return True
        else:
            return False

    


class Log(models.Model):
    created = models.DateTimeField()
    tag = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        db_table = "logs"
