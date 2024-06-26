from django.contrib import admin
from api.user.models import User, Department
from api.model.models import (Dataset, Model,Disease, Request,Question,Anwser,Response,
                              ResponseDetail,Notification, QuestionInstance)
from api.authentication.models.active_session import ActiveSession
from api.authentication.models.logs import Log

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("name","email","gender","username","password","permission")
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name","description")

# admin.site.register(User,UserAdmin)
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("path","class_num","train","test","val","classes")

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("path","accuracy","user","dataset","isActive")

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('image','user','created')
admin.site.register(Disease)
admin.site.register(Question)
admin.site.register(Anwser)
admin.site.register(Response)
admin.site.register(ResponseDetail)
admin.site.register(Notification)
admin.site.register(ActiveSession)
admin.site.register(Log)
admin.site.register(QuestionInstance)






