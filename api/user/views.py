import json
import jwt

from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from django.conf.global_settings import SECRET_KEY
from api.user.models import User
from api.authentication.views import (
    get_permission, 
    get_current_user,
    is_logged_in,
    is_supperuser
    )
from django.views.decorators.http import require_http_methods,require_GET,require_POST
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
# Create your views here.

@require_http_methods(['GET'])
def get_user_by_permission(request,permission):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"})
    p = get_permission(token=token)
    if p != 'admin':
        return JsonResponse({"msg":"permission not allowed"})
    try:
        # parse = parse_qs(request.GET.urlencode())
        # permission = parse['permission'][0]
        # print(permission)

        if permission is None:
            permission = "student"
        users  = list(User.objects.filter(permission=permission).values())
        return JsonResponse(users,safe=False)
    except:
        return JsonResponse({"msg":"do not match any user"})
    
@require_http_methods(['POST'])
def update_user_information(request):
    print(request.body)
    return JsonResponse({"msg":"update_user"})

@require_http_methods(["POST"])
@csrf_exempt
def change_password(request):
    password = request.POST.get("old-password")
    new_password = request.POST.get("new-password")
    # print(password,new_password)
    if(password is None or new_password is None):
        return JsonResponse({"msg":"password cannot empty"},status=status.HTTP_400_BAD_REQUEST)
    
    if password is new_password:
        return JsonResponse({"msg":"new password must different old password"},status=status.HTTP_400_BAD_REQUEST)
    
    is_logged = is_logged_in(token = request.COOKIES.get("token"))
    if is_logged:
        user_id = request.COOKIES.get("current_user")
      
        try:
            user =  User.objects.get(id=user_id)
            if(user.password != password):
                return JsonResponse({"msg":"password is not correct"},status=status.HTTP_400_BAD_REQUEST)
            
            user.password = new_password
            user.save()
            return JsonResponse({"msg":"change password successfull"},status=status.HTTP_200_OK)
        except:
            return JsonResponse({"msg":"Something wrong"},status=status.HTTP_501_NOT_IMPLEMENTED)
        # user = list(User.objects.filter(id=response["user_id"]))
    # not loggin user
    return JsonResponse({"msg":"not logged in"},status=status.HTTP_401_UNAUTHORIZED)

def get_user(request,id):
    if  not is_supperuser(request):
        return JsonResponse({"msg":"permission not allow"},status=status.HTTP_403_FORBIDDEN)
    print(id)
    # try:
    user = list(User.objects.filter(id=id).values())
    user = user[0]
    print(user)
    return JsonResponse({**user},status=status.HTTP_200_OK,safe=False)

    # except:
        # return JsonResponse({"msg":"user not found"},status=status.HTTP_404_NOT_FOUND)

def search_user(request):
    print(parse_qs(request.GET.urlencode()))
    query = parse_qs(request.GET.urlencode())
    print(query["name"])
    return JsonResponse({"msg":"helo"})