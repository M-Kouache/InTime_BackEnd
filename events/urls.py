from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/',views.SetUserProfile,name='UserProfile'),
    path('get_services/',views.get_Service,name='get_Service'),
]