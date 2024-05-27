from django.db import models
from datetime import datetime
class Log(models.Model):
    created = models.DateTimeField(default=datetime.now())
    tag = models.CharField(max_length=100)
    content = models.CharField(max_length=255)

    class Meta:
        db_table = "logs"