from django.db import models
from datetime import datetime
class Log(models.Model):
    choices = (
        ("LOGIN",'login'),
        ("LOGOUT","logout"),
        ("CREATE","create"),
        ("UPDATE","update"),
        ("DELETE","delete"),
        ("TRAIN","train")
    )
    created = models.DateTimeField(default=datetime.now())
    tag = models.CharField(max_length=100, choices=choices)
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = "logs"