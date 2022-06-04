from django.contrib import admin
from events.models import Events,Department,Service,UserProfile,Handler


# Register your models here.
@admin.register(Department)
class Departement(admin.ModelAdmin):
    list_display = ['id','libelle']

@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ['id','service','user']

@admin.register(Service)
class Service(admin.ModelAdmin):
    list_display = ['id','libelle','department']

@admin.register(Events)
class Events(admin.ModelAdmin):
    list_display = ['id','title','departement','public_events','date_start','date_end','actor','location']

@admin.register(Handler)
class Handler(admin.ModelAdmin):
    list_display = ['id','owner','user_handler']


