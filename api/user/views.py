from django.shortcuts import render
from rest_framework import status
from django.http import JsonResponse
from django.conf.global_settings import SECRET_KEY
from api.user.models import User
from api.authentication.views import get_permission
import jwt
# Create your views here.

def get_user_by_permission(request):
    token = request.COOKIES.get("token")
    if token is None:
        return JsonResponse({"msg":"must be logged in"})
    permission = get_permission(token=token)
    if permission != 'admin':
        return JsonResponse({"msg":"permission not allowed"})
    try:
        users  = list(User.objects.filter(permission=request.GET.get("user_type")).values())
        return JsonResponse(users,safe=False)
    except:
        return JsonResponse({"msg":"do not match any user"})