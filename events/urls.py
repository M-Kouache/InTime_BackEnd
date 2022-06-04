from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/',views.SetUserProfile,name='UserProfile'),
    path('get_services/',views.get_services,name='get_services'),
    path('me/',views.me,name='me'),
    path('add_handler/',views.addHandler,name='AddHandler'),
    path('remove_handler/',views.removeHandler,name='removeHandler'),
    path('events/<str:id>',views.UserEvents,name='UserEvents'),
    path('add_event/',views.addEvent,name='addEvent'),
    path('remove_event/',views.removeEvent,name='removeEvent'),
]