import jwt
import json
from datetime import datetime
from api.authentication.models.active_session import ActiveSession
from api.authentication.models.logs import Log
from api.user.models import User
from django.conf.global_settings import SECRET_KEY
from django.core import serializers
from datetime import datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,Http404, HttpResponseRedirect
from django.template import loader
from django.core.validators import validate_email

def genera_jwt_token(user):
    token = jwt.encode({"id":user.id,"exp":datetime.now()+timedelta(days=4),"permission":user.permission},SECRET_KEY)

    return token

def decode_token(token):
    return jwt.decode(token,SECRET_KEY,algorithms=["HS256"])

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
            token = genera_jwt_token(user)
            session.token  = token
            session.save()
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
        login_log("login",user=user)
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
    return JsonResponse(user[0],safe=False)

def get_permission(token):
    if(token is None):
        return JsonResponse({"msg":"not logged in"},Http404)
    res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    user = list(User.objects.filter(id=res["id"]).values())
    return user[0]["permission"]

@csrf_exempt
def register(request):
    name = request.POST.get("name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    re_password = request.POST.get("email")
    if password is None or password is re_password:
        return JsonResponse({"msg":"invalid password"})
    
    try:
        validate_email(email)
    except:
        return JsonResponse({"msg":"invalid email"})
    
    try:
        User.objects.get(username=username)
        return JsonResponse({"msg":"username already taken"})
    except:
        user = User.objects.create(name=name,username=username,email=email,password=password,permission="student")

    response = JsonResponse({"id":user.id,"name":name})
    return response

def login_log(tag,user):
    try:
        Log.objects.create(tag=tag,content="{user.name} just {tag} at {datetime.now}")
    except:
        pass

def is_supperuser(request):
    token = request.COOKIES.get("token")
    if token is None:
        return False
    
    permission = get_permission(token=token)
    if permission != 'admin':
        return False
    return True
    