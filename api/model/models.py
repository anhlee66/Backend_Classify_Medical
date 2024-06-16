from django.db import models
from api.user.models import User
from datetime import datetime

# Create your models here.
class Dataset(models.Model):
    path = models.CharField(max_length=255,unique=True)
    class_num = models.IntegerField()

    class Meta:
        db_table = "datasets"

class Model(models.Model):
    path = models.CharField(max_length=255,unique=True)
    accuracy = models.FloatField(default=0)
    created = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE,default=None)
    isActive = models.BooleanField(default=False)
    class Meta:
        db_table = 'models'

class Request(models.Model):
    image = models.CharField(max_length=255) # path to image
    content = models.CharField(max_length=255) #content request
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(default= datetime.now)
    class Meta:
        db_table = "requests"

class Response(models.Model):
    content = models.CharField(max_length=255)
    request = models.ForeignKey(Request,on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = "responses"


class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    type = models.CharField(max_length=100)

    class Meta:
        db_table = "diseases"

class ResponseDetail(models.Model):
    score = models.FloatField()
    response = models.ForeignKey(Response,on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.CASCADE)

    class Meta:
        db_table = "responseDetails"


