import jwt
import json
from api.authentication.models.active_session import ActiveSession
from api.user.models import User
from django.conf.global_settings import SECRET_KEY
from django.core import serializers
from datetime import datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,Http404, HttpResponseRedirect
from django.template import loader

def genera_jwt_token(user):
    token = jwt.encode({"id":user.id,"exp":datetime.now()+timedelta(days=4),"permission":user.permission},SECRET_KEY)

    return token

@csrf_exempt
def login(request):
    if(request.method == "GET"):
        token = request.COOKIES.get("token")
        if(token is None):
            return JsonResponse({"msg":"Not login, send template"})
        res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
       
        return JsonResponse({"msg":"logged in with permission {}".format(res["permission"])})
        

    if(request.method == "POST"):
        print(request)
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        if(username is None):
            return {"success":False,"msg":"Username is required to login"}
        
        if(password is None):
            return {"success":False,"msg":"password  is required to login"}
        
        user = User.authenticate(username = username, password = password)

        if user is None:
            return JsonResponse({"success":False,"msg":"Wrong identials"})
        
        try:
            session = ActiveSession.objects.get(user=user)
            token = session.token
            # if not session.token:
            #     raise ValueError
            jwt.decode(session.token,SECRET_KEY,algorithms=["HS256"])
            print(token)
        except (ObjectDoesNotExist,ValueError,jwt.ExpiredSignatureError):
           
            session = ActiveSession.objects.create(user=user, token= genera_jwt_token(user))

        response = JsonResponse({
            "success":True,
            "token":session.token,
            "user":{"id":user.id,"username":username}
        })
        response.set_cookie("token",session.token)
        response.set_cookie("current_user",user.id)
        return response

def logout(request):
    response = HttpResponseRedirect('login')
    response.delete_cookie("token")
    response.delete_cookie("current_user")
    return response


def get_current_user(request):
    token = request.COOKIES.get("token")
    if(token is None):
        return JsonResponse({"msg":"not logged in"},Http404)
    res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    user = list(User.objects.filter(id=res["id"]).values())
    print(user)
    return JsonResponse(user,safe=False)