from django.db import models
from api.user.models import User,Department
from datetime import datetime

# Create your models here.
class Disease(models.Model):
    name = models.CharField(max_length=100)
    label = models.TextField(max_length=500)
    concept = models.TextField(max_length=2000,null=True)
    reason = models.TextField(max_length=2000,null=True)
    symptom = models.TextField(max_length=2000,null=True)
    consequence = models.TextField(max_length=2000,null=True)
    type = models.CharField(max_length=200)

    class Meta:
        db_table = "diseases"

    def __str__(self) -> str:
        return self.name
class Dataset(models.Model):
    path = models.CharField(max_length=255,unique=True)
    class_num = models.IntegerField()
    train = models.FloatField()
    test = models.FloatField()
    val = models.FloatField()
    classes = models.CharField(max_length=1000,null=True, blank=True)

    class Meta:
        db_table = "datasets"
    def __str__(self) -> str:
        return self.path
    
class Model(models.Model):
    path = models.CharField(max_length=255,unique=True)
    accuracy = models.FloatField(default=0)
    created = models.DateTimeField(default=datetime.now())
    user = models.OneToOneField(User,blank=True, null=True,on_delete=models.SET_NULL)
    dataset = models.ForeignKey(Dataset,blank=True,null=True,on_delete=models.SET_NULL)
    isActive = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'models'

    def __str__(self) -> str:
        return self.path

class ModelDetails(models.Model):
    model = models.ForeignKey(Model,on_delete=models.CASCADE)    
    layer = models.IntegerField(default= 0 )
    parameter = models.IntegerField(default=0)
class Request(models.Model):
    image = models.CharField(max_length=255) # path to image
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created = models.DateTimeField(default= datetime.now())
    class Meta:
        db_table = "requests"

    def __str__(self) -> str:
        return self.user.name +' '+ self.created
    
class Response(models.Model):
    choices= (
        ("LIKE","like"),
        ("DISLIKE","dislike"),
        ("NORMAL","normal")
    )
    content = models.TextField(max_length=255)
    request = models.ForeignKey(Request,on_delete=models.CASCADE)
    created = models.DateTimeField(default=datetime.now())
    favorite = models.CharField(max_length=200,choices=choices,default="NORMAL")
    class Meta:
        db_table = "responses"

    def __str__(self) -> str:
        return self.request

class ResponseDetail(models.Model):
    score = models.FloatField()
    response = models.ForeignKey(Response,on_delete=models.CASCADE)
    disease = models.OneToOneField(Disease,null=True,blank=True,on_delete=models.SET_NULL)

    class Meta:
        db_table = "responseDetails"

    def __str__(self) -> str:
        return self.response +' ' +self.score

class Question(models.Model):
    tag_choices = (
        ("Da liễu","Da liễu"),
        ("Xương khớp","Xương khớp"),
        ("Não","Não")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.CharField(max_length=255) # path to image
    created = models.DateTimeField(default= datetime.now)
    content = models.TextField(max_length=1000,null=True)
    isAnwserd = models.BooleanField(default=False)
    tag = models.CharField(max_length=100,choices=tag_choices, default="Da liễu")
    class Meta:
        db_table = "questions"

    def __str__(self)-> str:
        return self.user.name + ': ' + self.content

class QuestionInstance(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "question_instance"

    def __str__(self) -> str:
        return self.question.__str__() + ':' + self.department.__str__()

class Anwser(models.Model):
    question = models.ForeignKey(QuestionInstance,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=1000,null=True)
    image = models.CharField(max_length=255,null=True)
    created = models.DateTimeField(default= datetime.now)
    disease = models.OneToOneField(Disease,null=True, on_delete=models.SET_NULL)
    class Meta:
        db_table ="anwsers"

    def __str__(self)-> str:
        return self.question + ' ' + self.content

class Notification(models.Model):
    choices = (
        ("information","Information"),
        ("warming","Warming"),
        ("error","Error")
    )
    tag = models.CharField(max_length=100,choices=choices,default="information")
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)

    class Meta:
        db_table = "notifications"

    def __str__(self)->str:
        return self.message