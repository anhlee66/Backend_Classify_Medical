from django.urls import path
from api.model.views import(
    get_all_diseases,
    create_new_disease,
    update_disease,
    search_disease
)
urlpatterns = [
    path("get_all_diseases",view=get_all_diseases,name="get_all_diseases"),
    path("create_new_disease",view=create_new_disease,name="create_new_disease"),
    path("<int:id>/update_disease",view=update_disease,name="update_disease"),
    path("search_disease",view=search_disease,name="search_disease")
]