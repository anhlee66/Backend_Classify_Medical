from django.db import models

# Create your models here.
class DiseaseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table='diseaseTypes'

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    type = models.ForeignKey(DiseaseType,on_delete=models.CASCADE)

    class Meta:
        db_table = "diseases"