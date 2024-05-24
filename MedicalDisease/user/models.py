from django.db import models

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
    class Meta:
        db_table = "users"
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table='roles'


class Account(models.Model):
    username  = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)

    class Meta: 
        db_table = 'accounts'


class Log(models.Model):
    created = models.DateTimeField()
    tag = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        db_table = "logs"