from django.db import models
from api.user.models import User
class ActiveSession(models.Model):
    choices = (
        ("ADMIN","admin"),
       ( "STUDENT","student"),
       ( "EXPERT","expert")
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permission = models.CharField(max_length=100,choices=choices,default="STUDENT")
    token = models.CharField(max_length=255)
    expire = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'active_sessions'