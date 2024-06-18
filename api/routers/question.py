from django.urls import path
from api.model.views import (
    send_question,
    get_all_question,
    send_anwser,
    get_all_anwser,
    get_anwser_by_user
)
urlpatterns = [
    path("request",view=send_question,name="send_question"),
    path("all/question",view=get_all_question,name="get_all_question"),
    path("anwser",view=send_anwser,name="send_anwser"),
    path("all/anwser",view=get_all_anwser, name="get_all_anwser"),
    path("user/<int:id>",view=get_anwser_by_user,name="get_anwser_by_id")
]