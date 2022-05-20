from rest_framework import serializers
from django.contrib.auth import get_user_model
from events.models import UserProfile,Events,Department,Service,Handler,Reciever,E_Notification



class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model =  get_user_model()
        fields = ['id','username','first_name','last_name','email','password']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department 
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id','service','user']

class HandlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Handler
        fields = "__all__"


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"



class RecieverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reciever
        fields = "__all__"



class E_NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = E_Notification
        fields = "__all__"


