from django.db import models
from api.user.models import User
class ActiveSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    permission = models.CharField(max_length=100,default="admin")
    token = models.CharField(max_length=255)
    expire = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'active_sessions'