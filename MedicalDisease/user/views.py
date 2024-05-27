from django.shortcuts import render
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.template import loader
from django.contrib.auth import login
from django.contrib.sessions.models import Session
from user.models import Account
from django.contrib.sessions.backends.db import SessionStore
from json import dumps
from .form import LoginForm
# Create your views here.
@csrf_protect
def login(request):
    if(request.method == "GET"):
        form = LoginForm()  
        template = loader.get_template('login.html')
        request.session.set_test_cookie()
        return HttpResponse(template.render({'form':form}))
    else:
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            form = LoginForm(request.POST)
            data = {'msg':'form not valid'}
            if(form.is_valid()):
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                try:
                    acc = Account.objects.get(username=username)
                except:
                    acc = None
                if(acc is not None and acc.check_password(password)):
                    request.session['user_id'] = acc.user.id
                    data = {'msg':'logged in'}
                    return HttpResponseRedirect('home')
                    
                else: 
                    data = {'msg':'something wrong'}
            
            return JsonResponse(data)  
        else:
            return HttpResponse("Please enable cookies and try again.")
        
       
         

        

def register(request):
    return JsonResponse({'msg':'signup'})

def logout(request):
    del request.session['user_id']
    return HttpResponseRedirect('login')
