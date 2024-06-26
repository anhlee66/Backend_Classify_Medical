from django.urls import path
from api.user.views import get_all_department
urlpatterns = [
    path("all",view=get_all_department,name="get_all_department")
]