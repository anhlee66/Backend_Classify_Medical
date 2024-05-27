from rest_framework import routers
from api.authentication.views import( 
    login,
    logout,
    get_current_user,
    register)
from api.user.views import get_user_by_permission
from django.urls import path, include
urlpatterns = [
    path("login",view=login,name='login'),
    path("logout",view=logout,name='logout'),
    path("get_current_user",view=get_current_user,name="get_current_user"),
    path("register",view=register,name="register"),
    path("get_all_user",view=get_user_by_permission,name="get_all_user")
]