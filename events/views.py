from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view
from events.models import Department,Service,UserProfile as BaseUserProfile , Events
from events.serializers import UserProfileSerializer,DepartmentSerializer,ServiceSerializer,UserAdminSerializer,EventsSerializer



#override djoser userViewSet behavior to add password checking logic.
class UserViewSet(DjoserUserViewSet):

    def create(self, request):
        user = self.queryset
        serializer = UserAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for pw in user:
            if check_password(serializer.data['password'], pw.password):
                raise serializers.ValidationError({"password":"this password already exists choose another one"})
        return super().create(request)



#route for getting or updating user profile
@api_view(['GET','PUT'])
def UserProfile(request):
    #if user exits return user and true else return false
    (user, created) = BaseUserProfile.objects.get_or_create(user=request.user)
    #check request type
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT': 
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
     
     
     
@api_view(['POST'])
def SetUserProfile(request):
    serializer = UserProfileSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST','GET'])
def UserEvents(request):
    if method == 'POST':
        serializer = EventsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
   

@api_view(['GET'])
def get_Service(request):
    service = Service.objects.all()
    serializer = ServiceSerializer(service,many=True)
    return Response(serializer.data)
