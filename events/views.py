from math import perm
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated , IsAdminUser, AllowAny
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from events.models import Department,Service,UserProfile as BaseUserProfile , Events, Handler
from events.serializers import UserProfileSerializer,DepartmentSerializer,ServiceSerializer,UserAdminSerializer,EventsSerializer, HandlerSerializer



#override djoser userViewSet behavior to add password checking logic and list all users.
class UserViewSet(DjoserUserViewSet):

    def create(self, request):
        user = get_user_model().objects.all()
        serializer = UserAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for pw in user:
            if check_password(serializer.data['password'], pw.password):
                raise serializers.ValidationError({"password":"this password already exists choose another one"})
        return super().create(request)
    
    def list (self,request):
        user = get_user_model().objects.all()
        serializer = UserAdminSerializer(user,many=True)
        return Response(serializer.data)



@api_view(['GET'])
def rootView(request):
    html= "<html><body style='height:80vh;display:flex;alignItems:center;justifyContent:center' ><h1 style='color:red;>Request not allowed</h1></body></html>"
    return HttpResponse(html)


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
     
     
     
@api_view(['POST','PUT'])
def SetUserProfile(request):
    (user, created) = BaseUserProfile.objects.update_or_create(user=request.user)

    '''if request.method == 'POST':
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)'''
    if request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        


@api_view(['POST','GET'])
def UserEvents(request,id):
   
    if  request.method == 'GET':

        data = []
        #get events for a specific user
        event_public = Events.objects.filter(public_events=True)
        event_private = Events.objects.filter(public_events=False,departement__isnull=True,actor=request.user)
        event_user_departement = Events.objects.filter(public_events=False,departement=id)
        event_data = event_public.union(event_private,event_user_departement,all=True)
        _Eventserializer = EventsSerializer(event_data,many=True)

        for _event in _Eventserializer.data:
            
            #get user profile information
            _userProfile = BaseUserProfile.objects.filter(user=_event['actor'])
            _UserProfileserializer = UserProfileSerializer(_userProfile,many=True)

            #get services information for that specific actor
            _services = Service.objects.filter(id=_UserProfileserializer.data[0]['service'])
            _ServiceSerializer = ServiceSerializer(_services,many=True)

            #get user information from auth user
            _user_auth = get_user_model().objects.filter(id=_event['actor'])
            _user_auth_serializer = UserAdminSerializer(_user_auth,many=True)

            #get departement information for that spicific actor
            _departement = Department.objects.filter(id = _ServiceSerializer.data[0]['department'])
            _department_serializer = DepartmentSerializer(_departement,many=True)

            data.append({
                'body':_event,
                'pub_info':_department_serializer.data[0],
                'user_info':_user_auth_serializer.data[0]
            })

        return JsonResponse({'events':data})


@api_view(['POST'])
def addEvent(request):
    
    if request.method == 'POST':
        serializer = EventsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 

@api_view(['POST'])
def removeEvent(request):
    if request.method == 'POST':
        event_deleted = Events.objects.filter(id=request.data['event']).delete()
        if event_deleted[0] > 0:
            return Response(status=200)
 

 
@api_view(['GET'])
def eventStatistics(request):
    events = Events.objects.all()
    serializer = EventSerializer(events, many=True)
    return render(request, 'admin/base.html',{serializer.data})



@api_view(['GET'])
def me(request):
    
    data = []

    #get user profile information
    _userProfile = BaseUserProfile.objects.filter(user=request.user)
    _UserProfileserializer = UserProfileSerializer(_userProfile,many=True)

    #get services information for that specific user
    _services = Service.objects.filter(id=_UserProfileserializer.data[0]['service'])
    _ServiceSerializer = ServiceSerializer(_services,many=True)

    #get user information from auth user
    _user_auth = get_user_model().objects.filter(id=_UserProfileserializer.data[0]['user'])
    _user_auth_serializer = UserAdminSerializer(_user_auth,many=True)

    #get departement information for that spicific actor
    _departement = Department.objects.filter(id = _ServiceSerializer.data[0]['department'])
    _department_serializer = DepartmentSerializer(_departement,many=True)

    #get all events handlers for that exact user    
    handlers = []
    _handler = Handler.objects.filter(owner = request.user)
    _handler_serializer = HandlerSerializer(_handler,many=True)
    for handler in _handler_serializer.data:
        _user_auth = get_user_model().objects.filter(id=handler['user_handler'])
        _user_handler_serializer = UserAdminSerializer(_user_auth,many=True)
        handlers.append(
            _user_handler_serializer.data[0]
        )

    handlings = []
    _handling = Handler.objects.filter(user_handler = request.user)
    _handling_serializer = HandlerSerializer(_handling,many=True)
    for handling in _handling_serializer.data:
        _user_auth = get_user_model().objects.filter(id=handling['owner'])
        _user_handling_serializer = UserAdminSerializer(_user_auth,many=True)
        handlings.append(
            _user_handling_serializer.data[0]
        )


    data.append({
        'department':_department_serializer.data[0],
        'info':_user_auth_serializer.data[0],
        'handlers':handlers,
        'handling':handlings
    })

    return Response({'user':data[0]})



@api_view(['POST'])
def addHandler(request):
    if request.method == 'POST' :
        serializer = HandlerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

       

@api_view(['POST'])
def removeHandler(request):
    if request.method == 'POST':
        nbr_handlers = request.data['user_handler']
        nbr_deleted = 0
        for handler in nbr_handlers:
            handler_deleted = None
            handler_deleted = Handler.objects.filter(owner=request.user,user_handler=handler).delete()
            nbr_deleted += handler_deleted[0]
        
        if nbr_deleted > 0:
            return Response(status=200)


     
@api_view(['GET'])
def get_services(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services,many=True)
    return Response(serializer.data)

