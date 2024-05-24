from django.db import models
from user.models import User
from disease.models import Disease
from datetime import datetime
# Create your models here.

class Request(models.Model):
    image = models.CharField(max_length=255) # path to image
    content = models.CharField(max_length=255) #content request
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        db_table = "requests"

class Response(models.Model):
    content = models.CharField(max_length=255)
    request = models.ForeignKey(Request,on_delete=models.CASCADE)

    class Meta:
        db_table = "responses"

class ResponseDetail(models.Model):
    score = models.FloatField()
    compare = models.CharField(max_length=255)  #path to compared image
    response = models.ForeignKey(Response,on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease,on_delete=models.CASCADE)
    class Meta:
        db_table = "responseDetails"