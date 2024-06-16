import jwt
import json
from datetime import datetime
from rest_framework import status
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
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        if(username is None):
            return {"success":False,"msg":"Username is required to login"}
        
        if(password is None):
            return {"success":False,"msg":"password  is required to login"}
        
        user = User.authenticate(username = username, password = password)

        if user is None:
            return JsonResponse({"success":False,"msg":"Wrong identials"},status=status.HTTP_400_BAD_REQUEST)
        
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
            "user":{"id":user.id,"username":username, 'permission':user.permission }
        },status=status.HTTP_200_OK)
        response.set_cookie("token",session.token)
        response.set_cookie("current_user",user.id)
        response.set_cookie("permission",user.permission)
        # response.set_cookie("csfrtoken",cs)
        login_log("login",user=user)
        return response

def logout(request):
    if not is_logged_in(request.COOKIES.get('token')):
        return JsonResponse({"success":False},status = status.HTTP_401_UNAUTHORIZED)
    response = JsonResponse({"success":True},status=status.HTTP_200_OK)
    response.delete_cookie("token")
    response.delete_cookie("current_user")
    return response


def get_current_user(request):
    token = request.COOKIES.get("token")
    if(token is None):
        return JsonResponse({"success":False,"msg":"not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    user = list(User.objects.filter(id=res["id"]).values())
    return JsonResponse({"success":True,**user[0]},status=status.HTTP_200_OK,safe=False)

def get_permission(token):
    if(token is None):
        return JsonResponse({"msg":"not logged in"},status=status.HTTP_401_UNAUTHORIZED)
    res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    user = list(User.objects.filter(id=res["id"]).values())
    return user[0]["permission"]

@csrf_exempt
def register(request):
    name = request.POST.get("name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    
    try:
        validate_email(email)
    except:
        return JsonResponse({"success":False,"msg":"invalid email"},status=status.HTTP_400_BAD_REQUEST)
    
    try:
        User.objects.get(username=username)
        return JsonResponse({"success":False,"msg":"username already taken"},status=status.HTTP_409_CONFLICT)
    except:
        user = User.objects.create(name=name,username=username,email=email,password=password,permission="student")

    response = JsonResponse({"success":True,"id":user.id,"name":name},status=status.HTTP_201_CREATED)
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
    
def is_logged_in(token):
    if(token is None):
        return False
    res = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
    users = list(User.objects.filter(id=res["id"]).values())
    user = users[0]
    if(user is None):
        return False
    return True
