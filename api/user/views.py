from django.shortcuts import render
from django.http import JsonResponse
from django.conf.global_settings import SECRET_KEY
import jwt
# Create your views here.

def get_current_user(request):
    token = request.COOKIES.get("token")
    if(token is None):
        return JsonResponse({"msg":"not logged in"})
    payload = jwt.decode(token,SECRET_KEY,algorithms=)