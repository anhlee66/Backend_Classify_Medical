"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core.view import (
    get_statistic,
    get_recent_loggedin)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/",include("api.routers.users"),name="api-users"),
    path("api/model/",include("api.routers.models"),name="api-model"),
    path("api/disease/",include("api.routers.disease"),name="api-disease"),
    path("api/statistic/",include("api.routers.statistic"),name="api-statistic"),
    path("api/question/",include("api.routers.question"),name="api-question"),
]
