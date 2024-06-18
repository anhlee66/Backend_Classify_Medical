from django.db import models
from api.user.models import User
from datetime import datetime

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length=500)
    concept = models.CharField(max_length=2000,null=True)
    reason = models.CharField(max_length=2000,null=True)
    symptom = models.CharField(max_length=2000,null=True)
    consequence = models.CharField(max_length=2000,null=True)
    type = models.CharField(max_length=200)

    class Meta:
        db_table = "diseases"

class Dataset(models.Model):
    path = models.CharField(max_length=255,unique=True)
    class_num = models.IntegerField()
    train = models.FloatField()
    test = models.FloatField()
    val = models.FloatField()
    classes = models.CharField(max_length=1000,default="")

    class Meta:
        db_table = "datasets"

class Model(models.Model):
    path = models.CharField(max_length=255,unique=True)
    accuracy = models.FloatField(default=0)
    created = models.DateTimeField(default=datetime.now())
    user = models.OneToOneField(User,blank=True, null=True,on_delete=models.SET_NULL)
    dataset = models.OneToOneField(Dataset,blank=True,null=True,on_delete=models.SET_NULL)
    isActive = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'models'

class Request(models.Model):
    image = models.CharField(max_length=255) # path to image
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(default= datetime.now())
    class Meta:
        db_table = "requests"

class Response(models.Model):
    choices= (
        ("LIKE","like"),
        ("DISLIKE","dislike"),
        ("NORMAL","normal")
    )
    content = models.CharField(max_length=255)
    request = models.ForeignKey(Request,on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())
    favorite = models.CharField(max_length=200,choices=choices,default="NORMAL")
    class Meta:
        db_table = "responses"



class ResponseDetail(models.Model):
    score = models.FloatField()
    response = models.ForeignKey(Response,on_delete=models.CASCADE)
    disease = models.OneToOneField(Disease,null=True,blank=True,on_delete=models.SET_NULL)

    class Meta:
        db_table = "responseDetails"

class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.CharField(max_length=255) # path to image
    created = models.DateTimeField(default= datetime.now)
    content = models.CharField(max_length=1000,null=True)
    isAnwserd = models.BooleanField(default=False)
    tag = models.CharField(max_length=300,default="")
    class Meta:
        db_table = "questions"

    
class Anwser(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.CharField(max_length=1000,null=True)
    image = models.CharField(max_length=255,null=True)
    created = models.DateTimeField(default= datetime.now)
    disease = models.OneToOneField(Disease,null=True,on_delete=models.SET_NULL,default=None)
    class Meta:
        db_table ="anwsers"


class Notification(models.Model):
    choices = (
        ("INFORMATION","information"),
        ("WARMING","warming"),
    )
    tag = models.CharField(max_length=100,choices=choices,default="INFORMATION")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)

    class Meta:
        db_table = "notifications"