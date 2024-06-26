from django.urls import path
from api.model.views import (
    get_request,
    train_model,
    get_all_model
    ,get_active_model,
    change_active_model
)
urlpatterns = [
    path("request",view=get_request,name="get_request"),
    path("train",view=train_model,name="train_model"),
    path("all",view=get_all_model,name="get_all_model"),
    path("active",view=get_active_model,name="get_active_model"),
    path("active/change",view=change_active_model,name=" change_active_model"),

]