from django.db import models
from user.models import User
from datetime import datetime
# Create your models here.
class Dataset(models.Model):
    path = models.CharField(max_length=255)
    class_num = models.IntegerField()

    class Meta:
        db_table = "datasets"

class Model(models.Model):
    path = models.CharField(max_length=255)
    accuracy = models.FloatField()
    created = models.DateTimeField(datetime.now())
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    dataset = models.ForeignKey(Dataset,on_delete=models.CASCADE)

    class Meta:
        db_table = 'models'