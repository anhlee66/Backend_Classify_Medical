from rest_framework import routers
from api.authentication.views import( 
    login,
    logout,
    get_current_user,
    register,
    )
from api.user.views import (
    get_user_by_permission,
    update_user_information,
    change_password,
    get_user,
    search_user
    )
from django.urls import path, include
urlpatterns = [
    path("login",view=login,name='login'),
    path("logout",view=logout,name='logout'),
    path("get_current_user",view=get_current_user,name="get_current_user"),   #get information of current user
    path("register",view=register,name="register"),   # sign up account for student
    path("get_all_user/<permission>",view=get_user_by_permission,name="get_all_user"),  #get all user with admin permission
    path("update_user",view=update_user_information,name="update_user_information"),
    path("change_password",view=change_password,name="change_password"),  # change password for current user
    path("<int:id>",view=get_user,name='get_user'),  #get user information with admin permission
    path("search",view=search_user,name="search_user") # search user information

]