from rest_framework import routers
from api.authentication.views import login,logout,get_current_user
from django.urls import path, include
urlpatterns = [
    path("login",view=login,name='login'),
    path("logout",view=logout,name='logout'),
    path("get_current_user",view=get_current_user,name="get_current_user")
]