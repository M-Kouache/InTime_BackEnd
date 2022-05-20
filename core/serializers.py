from django.contrib.auth.hashers import check_password
from djoser.serializers import SetPasswordRetypeSerializer as BaseSetPasswordRetypeSerializer, UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','first_name','last_name','email','password']


class UserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','username','first_name','last_name','email','is_staff','is_active']
