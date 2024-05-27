from django.urls import path
from api.model.views import (
    get_request,
    train_model,
    get_all_model
    ,get_active_model,
    get_all_dataset,
    get_all_diseases,
    create_new_disease
)
urlpatterns = [
    path("request",view=get_request,name="get_request"),
    path("train",view=train_model,name="train_model"),
    path("get_all_model",view=get_all_model,name="get_all_model"),
    path("get_active_model",view=get_active_model,name="get_active_model"),
    path("get_all_dataset",view=get_all_dataset,name="get_all_dataset"),
    path("get_all_diseases",view=get_all_diseases,name="get_all_diseases"),
    path("create_new_dataset",view=create_new_disease,name="create_new_disease")
]