from django.urls import path
from api.model.views import (
    get_all_dataset,
    view_more_image,
    add_data,
    get_dataset
)
urlpatterns = [
    path("all",view=get_all_dataset,name="get_all_dataset"),
    path("image",view=view_more_image,name="view_more_image"),
    path("<int:id>",view=get_dataset,name="get_dataset"),
    path("add_data",view=add_data,name="add_data"),
]