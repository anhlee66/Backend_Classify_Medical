from django.urls import path,include
from core.view import (
    get_statistic,
    get_recent_loggedin)

urlpatterns = [
    path("base",view=get_statistic,name='get_statistic'),
    path("recent_logged",view=get_recent_loggedin,name="get_recent_loggedin"),
   
]
