from django.urls import path
from api.model.views import (
    send_question,
    get_question_by_state,
    send_anwser,
    get_all_anwser,
    get_anwser_by_user,
    add_question_instance,
    get_question_by_process
)
urlpatterns = [
    path("request",view=send_question,name="send_question"),
    path("search",view=get_question_by_state,name="get_question_by_state"),
    path("process",view=get_question_by_process,name="get_question_py_process"),
    path("anwser",view=send_anwser,name="send_anwser"),
    path("all/anwser",view=get_all_anwser, name="get_all_anwser"),
    path("user/<int:id>",view=get_anwser_by_user,name="get_anwser_by_id"),
    path("<int:question_id>/department/<int:department_id>",view=add_question_instance, name="add_question_instance")
]