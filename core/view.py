import json
from datetime import datetime
from django.http import JsonResponse
from api.user.models import User
from api.model.models import Model, Dataset, Disease
from api.authentication.models.active_session import ActiveSession
from api.authentication.models.logs import Log
from rest_framework import status
def get_statistic(request):
    disease = Disease.objects.all().count()
    user = User.objects.all().count()
    dataset = Dataset.objects.all().count()
    model = Model.objects.all().count()
    data = {
        "user":user,
        "disease":disease,
        "dataset":dataset,
        "model":model}
    # print(data)
    return JsonResponse(data,status=status.HTTP_200_OK)

def get_recent_loggedin(request):
    logs = Log.objects.all().values()
    logs.reverse()
    # print(logs)
    data = []
    for log in logs:
        if(log["tag"] != "login"): continue 
        user = User.objects.get(id=log["content"])
        d: dict
        is_exists = False
        for d in data:
            if user.id in d.values():
                is_exists = True
        if is_exists:
            continue
        date : datetime
        try:
            ActiveSession.objects.get(user_id=user.id)
            status = "Online"
        except:
            status = "Offline"

        date = log["created"]
        data.append({"id":user.id,"user":user.name,"date":f'{date.strftime("%x")} {date.strftime("%X")}',"status":status})
        # print(data[0])
    data.reverse()
    return JsonResponse(data,safe=False)

